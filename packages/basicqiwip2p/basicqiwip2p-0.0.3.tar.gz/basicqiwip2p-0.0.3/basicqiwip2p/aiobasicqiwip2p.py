from httpx import AsyncClient
from basicqiwip2p.models import Response

import datetime
import json

class AioBasicQiwiP2P:
	"""
	AioQiwiAPI provides asynchronous and convenient
	functionality for working with QiwiP2P
	"""
	def __init__(self, p2p_key: str) -> None:
		self._headers = {
			'Authorization': f'Bearer {p2p_key}',
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		}

		self.client = AsyncClient(headers=self._headers)


	def _lifetime(self, minutes: int) -> str:
		""" You get the current time with added minutes """
		utc3 = datetime.timezone(datetime.timedelta(hours=3))
		now = datetime.datetime.now(utc3)

		expiration_date = now + datetime.timedelta(minutes=minutes)
		return expiration_date.strftime("%Y-%m-%dT%X")+'+03:00'



	async def new_bill(self, bill_id: str, amount: int, lifetime=15, comment='') -> dict:
		""" Creates a new invoice """
		url = f'https://api.qiwi.com/partner/bill/v1/bills/{bill_id}'
		data = {
			'amount': {
					'value': str(amount),
					'currency': 'RUB'
				},
			'comment': comment,
			'expirationDateTime': self._lifetime(minutes=lifetime)
		}

		response = (await self.client.put(url, json=data)).json()
		return Response.parse_obj(response)


	async def check(self, bill_id: str) -> dict:
		""" Gets invoice information """

		url = f'https://api.qiwi.com/partner/bill/v1/bills/{bill_id}'

		response = (await self.client.get(url)).json()
		return Response.parse_obj(response)


	async def is_paid(self, bill_id: str) -> bool:
		""" Checks whether the user has paid the invoice """
		check_data = await self.check(bill_id)
		
		if 'errorCode' in check_data:
			return #check_data['description']

		status = check_data['status']['value']
		return status == 'PAID'


	async def reject(self, bill_id: str) -> dict:
		""" Closes the invoice """
		url = f'https://api.qiwi.com/partner/bill/v1/bills/{bill_id}/reject'
		
		response = (await self.client.post(url)).json()
		return Response.parse_obj(response)

		
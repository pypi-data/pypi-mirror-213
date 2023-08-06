# BasicQiwiP2P
### Test version!

- [Project on PyPI](https://pypi.org/project/basicqiwip2p)
- [@mayneryt](https://vk.com/mayneryt) me

<br>
<details open>
<summary> <strong>Mini Documentation</strong> </summary><hr>
  
  <h3> Importing a synchronous or asynchronous class to work with </h3>
  
  ```
  from basicqiwip2p import AioBasicQiwiP2P  # Async
  from basicqiwip2p import BasicQiwiP2P     # Sync
  ```
  
  <p> New client </p>
  
  ```
  qiwip2p = BasicQiwiP2P(p2p_key='YOU_P2P_KEY')
  ```
  
  <br>
  <h3> New bill </h3>
  
  ```
  bill_id = "random-bill_id-1234"
  
  new_bill = qiwip2p.new_bill(
      bill_id=bill_id, 
      amount=100, 
      comment='For a good life!'
   )
  
  ```
  
  <h3> Checking bill for payment </h3>
  
  ```
  # -> bill_id = "random-bill_id-1234"
  
  is_paid = qiwip2p.is_paid(bill_id)
  # False or True
  ```
  
  <h3> Reject payment </h3>
  
  ```
  # -> bill_id = "random-bill_id-1234"
  
  qiwip2p.reject(bill_id)
  ```

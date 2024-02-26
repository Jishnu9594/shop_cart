var updateBtns = document.getElementsByClassName('update-cart')



for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('productId:', productId, 'action:', action)

    console.log('USER:', user)
   if(user === 'AnonymousUser'){
      addCookieItem(productId,action)


   }else{
       updateUserOrder(productId,action)

   }






    })
}
function addCookieItem(productId, action) {
   console.log('Not logged in')
   if (action == 'add') {
       if (cart[productId] == undefined) {
           cart[productId] = {'quantity': 1}
       } else {
           cart[productId]['quantity'] += 1
       }
   }
   if (action == 'remove') {
       cart[productId]['quantity'] -= 1
       if (cart[productId]['quantity'] <= 0) {
           console.log('Remove Item')
           delete cart[productId]
       }
   }
   console.log('Cart:', cart)

   // Update the cart in the cookie
   document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
   location.reload()
}




function updateUserOrder(productId, action) {
   console.log('Sending data..')

   var url = '/update_item/'
   var method = 'POST'
   var body = {
       'productId': productId,
       'action': action
   }

   if (user === 'AnonymousUser') {
       // For anonymous users, update the cart in cookies
       addCookieItem(productId, action)
       return
   }

   // For logged-in users, update the cart in the session
   fetch(url, {
       method: method,
       headers: {
           'Content-Type': 'application/json',
           'X-CSRFToken': csrftoken,
       },
       body: JSON.stringify(body)
   })
   .then(response => response.json())
   .then(data => {
       console.log('data:', data)
       location.reload()
   })
   .catch(error => {
       console.error('Error:', error)
   })
}
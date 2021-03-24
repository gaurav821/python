var updatebtn ;

updatebtn = $(".update-cart");

for(i=0; i<updatebtn.length;i++)
{   
        updatebtn[i].addEventListener('click',(function(){
        var productid = this.dataset.product
        var action = this.dataset.action
        console.log('productid:',productid,'action:',action)

        console.log('USER:', user)
        if(user == 'AnonymousUser'){
           addcookieitem(productid,action)
        }else{
            updateUserOrder(productid,action)
        }
    }))
}


function addcookieitem(productid,action){
    console.log('user isnt authenticated')

    if(action == 'add'){
        if(cart[productid]== undefined){
            cart[productid] = {'quantity':1}
        }

        else{
            cart[productid]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productid]['quantity'] -= 1


        if(cart[productid]['quantity'] <=0){
            console.log('item should be deleted')
            delete cart[productid];
        }
    }
    console.log('cart:',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) +";domain=;path/"
    location.reload()
}


function updateUserOrder(productid,action){
    console.log('user is authenticated,sending the data...')

    var url = '/update_item/'
    console.log('URL:',url)
    fetch(url,{
           method:'POST',
           headers:{
               'Content-Type':'application/json',
               'X-CSRFToken' : csrftoken,
           },
           body:JSON.stringify({'productid':productid,'action':action})
           
        } )
        .then((response) =>{
          return response.json()  
        })
        .then((data) =>{
        location.reload() /*console.log('Data:',data)*/ 
          });

}
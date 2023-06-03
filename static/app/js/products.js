let more = true
async function submit() {
    last = document.querySelectorAll('.product')[document.querySelectorAll('.product').length - 1].id
    console.log(last);
    csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
    data = JSON.stringify({last: last})
    let res = await fetch(location.href + '/more', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": csrf 
        },
        body: data
    })
    res = await res.json();
    images = res['images'];
    products = res['list'];
    categories = JSON.parse(res['categories'].replaceAll(`'`,`"`));
    shops = JSON.parse(res['shops'].replaceAll(`'`,`"`));
    products.forEach(product => {
        if (product.active) {
            newproduct = document.createElement('a');
            newproduct.setAttribute('href', ('products/' + product.id))
            newproduct.setAttribute('class', 'product')
            newproduct.setAttribute('id', product.id)
            newproduct_id = document.createElement('p')
            newproduct_id.setAttribute('class','id')
            newproduct_id.innerHTML = product.id;
            newproduct.appendChild(newproduct_id)
            newproduct_title = document.createElement('p')
            newproduct_title.setAttribute('class','name')
            newproduct_title.innerHTML = product.title;
            newproduct.appendChild(newproduct_title)
            newproduct_description = document.createElement('p')
            newproduct_description.setAttribute('class','name')
            newproduct_description.innerHTML = product.description;
            newproduct.appendChild(newproduct_description)
            images.forEach(img => {
                if (img.toproduct_id == product.id) {
                    newproduct_img = document.createElement('img')
                    newproduct_img.setAttribute('src', ('media/' + img.image))
                    newproduct_img.setAttribute('class', 'main')
                    newproduct.appendChild(newproduct_img)
                }
            });
            newproduct_shop = document.createElement('p')
            newproduct_shop.setAttribute('class','name')
            newproduct_shop.setAttribute('id', shops[product.id][0])
            newproduct_shop.innerHTML = shops[product.id][1];
            newproduct.appendChild(newproduct_shop)
            newproduct_categories = document.createElement('div')
            for (let i = 0; i < categories[product.id].length; i+=2){
                newproduct_category = document.createElement('p')
                newproduct_category.setAttribute('class','name')
                newproduct_category.setAttribute('id', categories[product.id][i])
                newproduct_category.innerHTML = categories[product.id][i + 1];
                newproduct_categories.appendChild(newproduct_category)
            }
            newproduct.appendChild(newproduct_categories)
            newproduct_amount = document.createElement('p')
            newproduct_amount.setAttribute('class','name')
            newproduct_amount.innerHTML = product.amount;
            newproduct.appendChild(newproduct_amount)
            newproduct_price = document.createElement('p')
            newproduct_price.setAttribute('class','name')
            newproduct_price.innerHTML = product.price;
            newproduct.appendChild(newproduct_price)
            document.querySelector('.products').appendChild(newproduct)
            more = true
        }
    });
}
onscroll = (event) => {
    if (window.pageYOffset + window.innerHeight >= document.documentElement.scrollHeight - 50 && more) {
        submit();
        more = false
    }
};
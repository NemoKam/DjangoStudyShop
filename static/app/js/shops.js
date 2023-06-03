let more = true
async function submit() {
    last = document.querySelectorAll('.shop')[document.querySelectorAll('.shop').length - 1].id
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
    shops = res['list'];
    console.log(shops);
    shops.forEach(shop => {
        newshop = document.createElement('a');
        newshop.setAttribute('href', ('shop/' + shop.id))
        newshop.setAttribute('id', shop.id)
        newshop.setAttribute('class', 'shop')
        newshop_id = document.createElement('h2')
        newshop_id.setAttribute('class','id')
        newshop_id.innerHTML = shop.id;
        newshop.appendChild(newshop_id)
        newshop_title = document.createElement('p')
        newshop_title.setAttribute('class','name')
        newshop_title.innerHTML = shop.title;
        newshop.appendChild(newshop_title)
        newshop_description = document.createElement('p')
        newshop_description.setAttribute('class','name')
        newshop_description.innerHTML = shop.description;
        newshop.appendChild(newshop_description)
        newshop_img = document.createElement('img')
        newshop_img.setAttribute('src',('media/' + shop.imageUrl))
        newshop.appendChild(newshop_img)
        document.querySelector('.shops').appendChild(newshop)
        more = true
        }
    );
}
onscroll = (event) => {
    if (window.pageYOffset + window.innerHeight >= document.documentElement.scrollHeight - 50 && more) {
        submit();
        more = false
    }
};
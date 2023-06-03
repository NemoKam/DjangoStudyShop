let more = true
async function submit() {
    last = document.querySelectorAll('.category')[document.querySelectorAll('.category').length - 1].id
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
    categories = res['list'];
    incategories = JSON.parse(res['categories'].replaceAll(`'`,`"`))
    categories.forEach(category => {
            newcategory = document.createElement('a');
            newcategory.setAttribute('href', ('category/' + category.id))
            newcategory.setAttribute('id', category.id)
            newcategory.setAttribute('class', 'category')
            newcategory_title = document.createElement('p')
            newcategory_title.setAttribute('class','name')
            newcategory_title.innerHTML = category.title;
            newcategory.appendChild(newcategory_title)
            newcategory_description = document.createElement('p')
            newcategory_description.setAttribute('class','name')
            newcategory_description.innerHTML = category.description;
            newcategory.appendChild(newcategory_description)
            newcategory_categories = document.createElement('div')
            for (let i = 0; i < incategories[category.id].length; i+=2){
                newcategory_category = document.createElement('p')
                newcategory_category.setAttribute('class','name')
                newcategory_category.setAttribute('id', incategories[category.id][i])
                newcategory_category.innerHTML = incategories[category.id][i + 1];
                newcategory_categories.appendChild(newcategory_category)
            }
            newcategory.appendChild(newcategory_categories)
            document.querySelector('.categories').appendChild(newcategory)
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
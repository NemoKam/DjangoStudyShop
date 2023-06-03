from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.utils.translation import gettext as _
from .forms import ShopForm, CategoryForm, ProductForm, MakeWatermarkForm, RegisterForm, LoginForm, SendMoneyForm
from .models import Shop, Category, Product, ProductImages, MakeWatermark, Profile
from .tasks import make_watermark_task
from decimal import Decimal
import json

def main_view(request):
    shops = Shop.objects.all()
    user_ip = request.META.get("REMOTE_ADDR")
    return render(request, 'app/main.html', {'list': shops})

def shops_view(request):
    try:
        from_id = request.GET['fromid']
    except:
        from_id = Shop.objects.first().id
    try:
        to_id = request.GET['toid']
    except:
        to_id = Shop.objects.last().id
    shops = Shop.objects.filter(id__range=[from_id, to_id])[:5]
    return render(request, 'app/shops.html', {'list': shops, 'type': 'shop'})

def new_shop_view(request):
    if request.method == 'GET':
        form = ShopForm()
        return render(request, 'app/create.html', {'form': form})
    else:
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            image_url = request.FILES['image_url']
            shop = Shop.objects.create(title=title, description=description, image_url=image_url)
            shop.save()
            return redirect(shops_view)
        else:
            return HttpResponse('error') 

def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'app/categories.html', {'list': categories, 'type': 'category'})

def new_category_view(request):
    if request.method == 'GET':
        form = CategoryForm()
        all_category = Category.objects.all()
        return render(request, 'app/create.html', {'form': form, 'categories': all_category})
    else:
        form = CategoryForm(request.POST)
        if form.is_valid():
            categoryIn = request.POST.getlist('in_category')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            category = Category.objects.create(title=title, description=description)
            category.save()
            for parent in categoryIn:
                category.in_category.add(get_object_or_404(Category, id=int(parent)))
            return redirect(categories_view)
        else:
            return HttpResponse('error') 

def products_view(request):
    products = Product.objects.filter(active=True).order_by("id")[:5]
    images = ProductImages.objects.filter(to_product__in=list(products.values_list('id', flat=True)), is_main=True)
    for i in images:
        print(i.image)
    return render(request, 'app/products.html', {'list': products, 'type': 'product', 'images': images})

def new_product_view(request):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'app/create.html', {'form': form})
    else:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            in_shop = request.POST['in_shop']
            in_category = request.POST.getlist('in_category')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            images = request.FILES.getlist('images')
            amount = form.cleaned_data.get('amount')
            price = form.cleaned_data.get('price')
            active = form.cleaned_data.get('active')
            product = Product.objects.create(in_shop_id=in_shop, title=title, description=description, amount=amount, price=price, active=active)
            product.save()
            for category in in_category:
                product.in_category.add(get_object_or_404(Category, id=int(category)))
            for image in range(len(images)):
                if image == 0:
                    productImage = ProductImages.objects.create(to_product=product, image=images[image], is_main=True)
                else:
                    productImage = ProductImages.objects.create(to_product=product, image=images[image], is_main=False)
                productImage.save()
            return redirect(products_view)
        else:
            return HttpResponse('error') 

def more_view(request, typ):
    if typ == 'products':
        last_id = json.loads(request.body.decode('utf-8'))['last']
        products = Product.objects.filter(id__gt=int(last_id),active=True)[:5]
        shops = {}
        categories = {}
        for product in products:
            product_category = []
            product_shop = [product.in_shop.id, product.in_category.title]
            for category in product.in_category.all():
                product_category.append(category.id)
                product_category.append(category.title)
            categories[f"{product.id}"] = product_category
            shops[f"{product.id}"] = product_shop
        images = ProductImages.objects.filter(to_product__in=list(products.values_list('id', flat=True)), is_main=True)
        return JsonResponse({'list': list(products.values()), 'images': list(images.values()), 'categories': str(categories), 'shops': str(shops)})
    if typ == 'shops':
        lastid = json.loads(request.body.decode('utf-8'))['last']
        shops = Shop.objects.filter(id__gt=int(lastid))[:5]
        return JsonResponse({'list': list(shops.values())})
    if typ == 'categories':
        lastid = json.loads(request.body.decode('utf-8'))['last']
        categories = Category.objects.filter(id__gt=int(lastid))[:5]
        categoriesParents = {}
        for category in categories:
            categoryInCategories = []
            for incategory in category.categoryIn.all():
                categoryInCategories.append(incategory.id)
                categoryInCategories.append(incategory.title)
            categoriesParents[f"{category.id}"] = categoryInCategories
        return JsonResponse({'list': list(categories.values()), 'categories': str(categoriesParents)})

def info_view(request, typ, pk):
    if typ == 'products':
        product = get_object_or_404(Product, id=pk)
        images = ProductImages.objects.filter(toproduct=product.id)
        return render(request, 'app/info.html', {'product': product, 'images': images})

@login_required
def make_watermark_view(request):
    if request.method == 'GET':
        form = MakeWatermarkForm()
        maden = MakeWatermark.objects.filter(to_user=request.user)[:5]
        return render(request, 'app/makeWaterMark.html', {"form": form, 'maden': maden})
    else:    
        # try:
        to_user = request.user
        image_before = request.FILES['image_before']
        maden_watermark = MakeWatermark.objects.create(to_user=to_user, image_before=image_before)
        maden_watermark.save()
        make_watermark_task.delay(maden_watermark.id)
        return HttpResponse('wait')

def register_view(request):
    if request.user.is_authenticated:
        return HttpResponse(_('You alredy logged in'))
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                repeat_password = form.cleaned_data.get('repeat_password')
                if User.objects.filter(username=username):
                    return HttpResponse(_('Username is already taken'))
                if User.objects.filter(email=email):
                    return HttpResponse(_('Email is already taken!'))
                if password == '':
                    return HttpResponse(_('Password is empty!'))
                if password != repeat_password:
                    return HttpResponse(_('Passwords are different!'))
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                name = form.cleaned_data.get('name')
                surname = form.cleaned_data.get('surname')
                about = form.cleaned_data.get('about')
                avatar = request.FILES['avatar']
                balance = 0.00
                profile = Profile.objects.create(user=user, name=name, surname=surname, about=about, avatar=avatar, balance=balance)
                profile.save()
                return redirect(login_view)
            except:
                return HttpResponse('error')
        else:
            return HttpResponse('error') 
    else:
        form = RegisterForm()
        return render(request, 'app/auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponse(_('You alredy logged in'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                else:
                    return HttpResponse(_('Incorrect username or password'))
            else:
                return HttpResponse(_('Empty username or password'))
            return redirect(main_view)
        else:
            return HttpResponse(_('Invalid form'))
    else:
        form = LoginForm()
        return render(request, 'app/auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect(main_view)

@login_required
def add_money_view(request, moneyToAdd):
    balance = get_object_or_404(Profile, user=request.user).balance
    balance += Decimal(moneyToAdd)
    Profile.objects.filter(user=request.user).update(balance=balance)
    return HttpResponse('2')

@login_required
def check_balance_view(request):
    balance = Profile.objects.get(user=request.user).balance
    return HttpResponse(balance)

@transaction.atomic
def create_transaction_view(request, form):
    money = form.cleaned_data.get('money')
    to_user = form.cleaned_data.get('to_user')
    from_user = request.user
    sid = transaction.savepoint()
    if 1:
        transaction.savepoint_commit(sid)
    else:
        transaction.savepoint_rollback(sid)
    return HttpResponse('fe')


@login_required
def send_money_view(request):
    if request.method == 'POST':
        form = SendMoneyForm(request.POST)
        if form.is_valid():
            create_transaction_view(request, form)
            return HttpResponse('wait')
        else:
            return HttpResponse('error')
    else:
        form = SendMoneyForm()
        balance = Profile.objects.get(user=request.user).balance
        return render(request, 'app/transactions/sendMoney.html', {'form': form, 'balance': balance})

@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'app/profile/profile.html', {'profile': profile})
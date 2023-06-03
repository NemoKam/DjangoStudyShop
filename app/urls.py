from .views import main_view, new_shop_view, shops_view, new_category_view, categories_view, new_product_view, products_view, more_view, info_view, make_watermark_view, register_view, login_view, logout_view, add_money_view, check_balance_view, profile_view, send_money_view
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', main_view),
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('register/', register_view),
    path('logout/', logout_view),
    path('shop/new/', new_shop_view),
    path('shop/', shops_view),
    path('category/new/', new_category_view),
    path('category/', categories_view),
    path('product/new/', new_product_view),
    path('product/', products_view),
    path('<str:typ>/more/', more_view),
    path('<str:typ>/<int:pk>/', info_view),
    path('makeWatermark/', make_watermark_view),
    path('addMoney/<str:moneyToAdd>/', add_money_view),
    path('sendMoney/', send_money_view),
    path('checkBalance/', check_balance_view),
    path('profile/', profile_view),
] 
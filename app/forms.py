from django import forms
from .models import Shop, Product, Category, MakeWatermark, Profile, Transaction


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ["title", "description", "image_url"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["in_category", "title", "description"]


class ProductForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Product
        fields = ["in_shop", "in_category", "title",
                  "description", "amount", "price", "active"]


class MakeWatermarkForm(forms.ModelForm):
    class Meta:
        model = MakeWatermark
        fields = ["image_before"]


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ["name", "surname", "about", "avatar"]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class SendMoneyForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["to_user", "money"]
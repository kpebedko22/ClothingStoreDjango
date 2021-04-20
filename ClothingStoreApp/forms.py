from django import forms
from .models import Clothes, Size, Color, Category, Order, Cart, CartItem, Customer, Gender, MainCategory, SubCategory

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class ClothesForm(forms.ModelForm):

    name = forms.CharField(max_length=100, required=True, label='')
    name.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Наименование'
    })

    PK_Category = forms.ModelChoiceField(queryset=Category.objects.all(
    ), label='', required=True, empty_label='Категория')
    PK_Category.widget.attrs.update({'class': 'form-control btn-outline-none'})

    PK_MainCategory = forms.ModelChoiceField(queryset=MainCategory.objects.all(
    ), label='', required=True, empty_label='Основная категория')
    PK_MainCategory.widget.attrs.update({'class': 'form-control btn-outline-none'})

    PK_SubCategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(
    ), label='', required=True, empty_label='Подкатегория')
    PK_SubCategory.widget.attrs.update({'class': 'form-control btn-outline-none'})

    PK_Size = forms.ModelChoiceField(
        queryset=Size.objects.all(), label='', required=True, empty_label='Размер')
    PK_Size.widget.attrs.update({'class': 'form-control btn-outline-none'})

    PK_Color = forms.ModelChoiceField(
        queryset=Color.objects.all(), label='', required=True, empty_label='Цвет')
    PK_Color.widget.attrs.update({'class': 'form-control btn-outline-none'})

    price = forms.DecimalField(decimal_places=2, label='', required=True)
    price.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Цена',
        'min': '0'
    })

    imagePath = forms.ImageField(label='Фото:', required=False)
    imagePath.widget.attrs.update({'class': 'form-control btn-outline-none'})

    description = forms.CharField(
        label='', widget=forms.Textarea, required=True)
    description.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Описание'
    })

    """ slug = forms.SlugField()
    slug.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'URL'
    }) """

    class Meta:
        model = Clothes
        fields = ['PK_Clothes', 'name', 'PK_MainCategory', 'PK_SubCategory', 'PK_Category',
                  'PK_Size', 'PK_Color', 'price', 'imagePath', 'description']

        exclude = ['slug']


class OrderForm(forms.ModelForm):
    nameCustomer = forms.CharField(max_length=255, required=True, label='')
    nameCustomer.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Имя'
    })

    phoneCustomer = forms.CharField(max_length=100, required=True, label='')
    phoneCustomer.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Телефон'
    })

    emailCustomer = forms.EmailField(max_length=254, required=True, label='')
    emailCustomer.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'E-mail'
    })

    cart = forms.ModelChoiceField(
        queryset=Cart.objects.all(), label='', required=False)
    cart.widget.attrs.update({'hidden': 'true'})

    class Meta:
        model = Order
        fields = ['PK_Order', 'nameCustomer',
                  'phoneCustomer', 'emailCustomer', 'cart']


class AccountDataForm(forms.ModelForm):
    name = forms.CharField(max_length=255, label='Имя', required=False)
    name.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Имя'
    })

    midname = forms.CharField(max_length=255, label='Отчество', required=False)
    midname.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Отчество'
    })

    surname = forms.CharField(max_length=255, label='Фамилия', required=False)
    surname.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Фамилия'
    })

    phone = forms.CharField(max_length=100, label='Телефон', required=False)
    phone.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Телефон'
    })

    email = forms.EmailField(max_length=254, label='E-mail', required=False)
    email.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'E-mail'
    })

    birthday = forms.DateField(required=False, label='Дата рождения',
                               widget=forms.DateInput(attrs={
                                   'class': 'form-control btn-outline-none',
                                   'type': 'date'
                               }))

    PK_Gender = forms.ModelChoiceField(
        queryset=Gender.objects.all(), label='Пол', empty_label='Пол', required=False)
    PK_Gender.widget.attrs.update({'class': 'form-control btn-outline-none'})

    class Meta:
        model = Customer
        fields = ['PK_Customer', 'name', 'midname', 'surname',
                  'phone', 'email', 'birthday']


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(max_length=255, required=True, label='')
    username.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Логин'
    })

    password = forms.CharField(
        max_length=255, required=True, label='', widget=forms.PasswordInput())
    password.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Пароль'
    })


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    name = forms.CharField(max_length=255, required=True, label='')
    name.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Имя'
    })

    email = forms.EmailField(max_length=254, required=True, label='')
    email.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'E-mail'
    })

    username = forms.CharField(max_length=255, required=True, label='')
    username.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Логин'
    })

    password1 = forms.CharField(
        max_length=255, required=True, label='', widget=forms.PasswordInput())
    password1.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Пароль'
    })

    password2 = forms.CharField(
        max_length=255, required=True, label='', widget=forms.PasswordInput())
    password2.widget.attrs.update({
        'class': 'form-control btn-outline-none',
        'placeholder': 'Повторите пароль'
    })

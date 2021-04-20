from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Clothes, Order, Cart, MainCategory, SubCategory, Category, Color, Size, CartItem
from .forms import ClothesForm, OrderForm, UserLoginForm, UserRegistrationForm, AccountDataForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.utils import timezone
import datetime


def getCategories():
    res = []
    mainCategories = MainCategory.objects.all()

    for mc in mainCategories:

        myDict = dict()
        myDict['MainCategory'] = mc
        myDict['SubCategories'] = list()

        subCategories = SubCategory.objects.all()

        for sc in subCategories:

            myDict2 = dict()
            myDict2['SubCategory'] = sc

            categories = Category.objects.filter(
                PK_MainCategory=mc, PK_SubCategory=sc)

            myDict2['Categories'] = categories
            myDict['SubCategories'].append(myDict2)

        res.append(myDict)
    return res


def getTitle(mc=None, sc=None, c=None):

    # если сабкатегория не выбрана - значит вся одежда
    if sc is None:
        return '{}: одежда и аксессуары'.format(mc.name)

    # если категория не выбрана - значит одежда или аксессуары
    if c is None:
        return '{}: {}'.format(mc.name, sc.name)

    # иначе - фул категория
    return '{}: {}'.format(mc.name, c.name)


def index(request):

    return render(request, 'index.html', {
        'cart': Cart.objects.all().last(),
        'categories': getCategories()
    })


def catalog(request, slug_MainCat=None, slug_SubCat=None, slug_Cat=None):
    mc, sc, c = None, None, None

    clothes = Clothes.objects.all()

    if slug_MainCat:
        mc = MainCategory.objects.get(slug=slug_MainCat)
        clothes = clothes.filter(PK_MainCategory=mc)

    if slug_SubCat:
        sc = SubCategory.objects.get(slug=slug_SubCat)
        clothes = clothes.filter(PK_SubCategory=sc)

    if slug_Cat:
        c = Category.objects.get(slug=slug_Cat)
        clothes = clothes.filter(PK_Category=c)

    if request.is_ajax():
        data = []
        for item in clothes:
            data.append({
                'PK_Clothes': item.PK_Clothes,
                'name': item.name,
                'price': item.price,
                'imagePath': item.imagePath.url,
                'color': item.PK_Color.PK_Color,
                'size': item.PK_Size.PK_Size,
                'absolute_url': item.get_absolute_url()
            })
        return JsonResponse(data, safe=False)

    colors = []
    sizes = []
    for item in clothes:
        if item.PK_Color not in colors:
            colors.append(item.PK_Color)
        if item.PK_Size not in sizes:
            sizes.append(item.PK_Size)

    return render(request, 'catalog.html', {
        "clothes": clothes,
        'cart': Cart.objects.all().last(),
        'categories': getCategories(),
        'colors': colors,
        'sizes': sizes,
        'category_title': getTitle(mc, sc, c),
        'breadcrumbs': {'MainCategory': mc, 'SubCategory': sc, 'Category': c}
    })


def single_product(request, slug_MainCat=None, slug_SubCat=None, slug_Cat=None, slug_Clothes=None):
    currentItem = Clothes.objects.get(slug=slug_Clothes)
    return render(request, 'single-product.html', {
        "singleItem": currentItem,
        'cart': Cart.objects.all().last(),
        'categories': getCategories()
    })


@login_required
def products_administration(request):

    if request.user.is_superuser:

        return render(request, 'products-administration.html', {
            "clothes": Clothes.objects.all(),
            'cart': Cart.objects.all().last(),
            'categories': getCategories()
        })

    return redirect('/index')


@login_required
def add_to_db(request):
    # добавление товара в бд

    if request.method == 'POST':
        # создание формы с заполненными полями
        form = ClothesForm(request.POST, request.FILES)

        if form.is_valid():
            # запись в базу
            form.save()

            # переход к странице администрирования
            return HttpResponseRedirect('/products-administration')

    # создание пустой формы
    form = ClothesForm()
    return render(request, "product-editing.html", {
        'form': form,
        'cart': Cart.objects.all().last(),
        'categories': getCategories()
    })


@login_required
def delete_from_db(request, item):
    # удаление товара из бд

    currentItem = Clothes.objects.get(PK_Clothes=item)
    currentItem.delete()
    return HttpResponseRedirect('/products-administration')


@login_required
def edit_in_db(request, item):
    # редактирование товара в бд

    currentItem = Clothes.objects.get(PK_Clothes=item)

    if request.method == 'POST':
        # создание формы с заполненными полями
        form = ClothesForm(request.POST, request.FILES)

        if form.is_valid():

            # изменение полей
            currentItem.name = form.cleaned_data["name"]
            currentItem.PK_MainCategory = form.cleaned_data["PK_MainCategory"]
            currentItem.PK_SubCategory = form.cleaned_data["PK_SubCategory"]
            currentItem.PK_Category = form.cleaned_data["PK_Category"]
            currentItem.PK_Size = form.cleaned_data["PK_Size"]
            currentItem.PK_Color = form.cleaned_data["PK_Color"]
            currentItem.price = form.cleaned_data["price"]
            currentItem.imagePath = form.cleaned_data["imagePath"]
            currentItem.description = form.cleaned_data["description"]

            # запись модели
            currentItem.save()
            return HttpResponseRedirect('/products-administration')

    # создание формы с заполнением полей данными модели
    form = ClothesForm(instance=currentItem)
    return render(request, "product-editing.html", {
        'form': form,
        'PK': currentItem.PK_Clothes,
        'cart': Cart.objects.all().last(),
        'categories': getCategories()
    })


def cart(request):
    # страница оформления заказа

    cart = Cart.objects.all().last()
    if request.method == 'POST':
        # создание формы с заполненными полями
        form = OrderForm(request.POST)
        if form.is_valid():

            # проверяем что в корзине есть товары
            # чтобы не добавлять заказы с пустой корзиной в бд
            if cart.totalItems:
                # добавляем в объект заказа текущую корзину, юзера и дату...
                # и сохраняем
                newOrder = form.save(commit=False)
                newOrder.PK_Cart = cart

                # если покупатель выполнил вход - то для заказа указываем его
                if request.user.is_authenticated:
                    newOrder.PK_Customer = request.user.profile

                newOrder.date = datetime.datetime.now(
                    tz=timezone.get_current_timezone())
                newOrder.save()

                # создаем новую корзину для товаров
                newCart = Cart()
                newCart.save()

            # обновляем страницу заказа
            return HttpResponseRedirect('/cart')

    # если юзер выполнил вход - берем его данные
    if request.user.is_authenticated:
        name = ''
        phone = ''
        email = ''
        if request.user.profile.name:
            name = request.user.profile.name
        if request.user.profile.phone:
            phone = request.user.profile.phone
        if request.user.profile.email:
            email = request.user.profile.email
        form = OrderForm(
            initial={'nameCustomer': name, 'phoneCustomer': phone, 'emailCustomer': email})

    # иначе создание пустой формы
    else:
        form = OrderForm()

    return render(request, 'cart.html', {'cart': cart, 'form': form})


def add_to_cart(request, item):
    # добавление товара в корзину

    currentItem = Clothes.objects.get(PK_Clothes=item)

    # если корзины для товаров нет, то создаем новую
    # иначе берем последнюю
    # (предполагается что заказа с этой корзиной не было)
    if not Cart.objects.all():
        currentCart = Cart()
        currentCart.save()
    else:
        currentCart = Cart.objects.all().last()

    cartItem = CartItem()
    cartItem.name = currentItem.name
    cartItem.PK_Size = currentItem.PK_Size
    cartItem.PK_Color = currentItem.PK_Color
    cartItem.price = currentItem.price
    cartItem.imagePath = currentItem.imagePath
    cartItem.save()

    currentCart.items.add(cartItem)
    currentCart.UpdateTotal()

    return HttpResponseRedirect('/cart')


def delete_from_cart(request, item):
    # удаление товара из корзины

    currentCart = Cart.objects.all().last()
    currentCart.items.remove(item)
    currentCart.UpdateTotal()
    return HttpResponseRedirect('/cart')


""" Страницы личного кабинета """


@login_required
def account(request):
    return render(request, 'account.html', {
        'cart': Cart.objects.all().last(),
        'categories': getCategories(),
        'orders': Order.objects.filter(PK_Customer=request.user.profile.PK_Customer).order_by('-date')
    })


@login_required
def account_data(request):
    customer = request.user.profile

    if request.method == 'GET':

        form = AccountDataForm(initial={
            'name': customer.name,
            'midname': customer.midname,
            'surname': customer.surname,
            'phone': customer.phone,
            'email': customer.email,
            'birthday': customer.birthday,
            'PK_Gender': customer.PK_Gender
        })
        return render(request, 'account-data.html', {
            'cart': Cart.objects.all().last(),
            'categories': getCategories(),
            'form': form
        })
    elif request.method == 'POST':

        form = AccountDataForm(request.POST)
        if form.is_valid():

            customer.name = form.cleaned_data['name']
            customer.midname = form.cleaned_data['midname']
            customer.surname = form.cleaned_data['surname']
            customer.phone = form.cleaned_data['phone']
            customer.email = form.cleaned_data['email']
            customer.birthday = form.cleaned_data['birthday']
            customer.PK_Gender = form.cleaned_data['PK_Gender']

            customer.save()

            return redirect('account-data')

        return redirect('account-data')


""" END Страницы личного кабинета """

""" Регистрация, логин, логаут """


def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'login.html', {'form': UserLoginForm(), 'titlePage': 'Вход', 'titleButton': 'Войти'})

    elif request.method == 'POST':
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'login.html', {'form': UserLoginForm(), 'error': 'Логин и/или пароль не подходят...', 'titlePage': 'Вход', 'titleButton': 'Войти'})
        else:
            login(request, user)
            return redirect('account')


def registration_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'login.html', {'form': UserRegistrationForm(), 'titlePage': 'Регистрация', 'titleButton': 'Зарегистрироваться'})

    elif request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            if user is None:
                return render(request, 'login.html', {'form': UserRegistrationForm(), 'error': 'Ошибка регистрации...', 'titlePage': 'Регистрация', 'titleButton': 'Зарегистрироваться'})
            else:
                user.profile.name = form.cleaned_data.get('name')
                user.profile.email = form.cleaned_data.get('email')
                login(request, user)
                return redirect('account')

    return redirect('index')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


""" END Регистрация, логин, логаут """


""" def error404(request):
    return HttpResponseRedirect('/index') """

from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# для генерации слагов через бэкенд (для Clothes)
from unidecode import unidecode
from django.template.defaultfilters import slugify

# Модели БД магазина одежды


class Size(models.Model):
    PK_Size = models.AutoField(db_column='PK_Size', primary_key=True)
    name = models.CharField(db_column='sizeName',
                            max_length=100, verbose_name='Наименование')

    class Meta:
        db_table = 'Size'
        verbose_name_plural = 'Размеры одежды'
        verbose_name = 'Размер одежды'

    def __str__(self):
        return self.name


class MainCategory(models.Model):
    PK_MainCategory = models.AutoField(
        db_column='PK_MainCategory', primary_key=True)
    name = models.CharField(
        db_column='name', max_length=100, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")

    class Meta:
        db_table = 'MainCategory'
        verbose_name_plural = 'Главные категории'
        verbose_name = 'Главная категория'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog-main-category', kwargs={'slug_MainCat': self.slug})


class SubCategory(models.Model):
    PK_SubCategory = models.AutoField(
        db_column='PK_SubCategory', primary_key=True)
    name = models.CharField(
        db_column='name', max_length=100, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")

    class Meta:
        db_table = 'SubCategory'
        verbose_name_plural = 'Подкатегории'
        verbose_name = 'Подкатегория'

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self, mc):
        return reverse('catalog-sub-category', kwargs={'slug_MainCat': mc.slug, 'slug_SubCat': self.slug})


class Category(models.Model):
    PK_Category = models.AutoField(db_column='PK_Category', primary_key=True)
    PK_MainCategory = models.ForeignKey(
        MainCategory, models.DO_NOTHING, db_column='PK_MainCategory', verbose_name='Главная категория')
    PK_SubCategory = models.ForeignKey(
        SubCategory, models.DO_NOTHING, db_column='PK_SubCategory', verbose_name='Подкатегория')

    name = models.CharField(
        db_column='name', max_length=100, verbose_name='Наименование')

    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")

    class Meta:
        db_table = 'Category'
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self):
        return "{} - {} - {}".format(self.PK_MainCategory, self.PK_SubCategory, self.name)

    def get_absolute_url(self):
        return reverse('catalog-category', kwargs={'slug_MainCat': self.PK_MainCategory.slug, 'slug_SubCat': self.PK_SubCategory.slug, 'slug_Cat': self.slug})


class Color(models.Model):
    PK_Color = models.AutoField(db_column='PK_Color', primary_key=True)
    name = models.CharField(db_column='colorName',
                            max_length=100, verbose_name='Наименование')

    class Meta:
        db_table = 'Color'
        verbose_name_plural = 'Цвета'
        verbose_name = 'Цвет'

    def __str__(self):
        return self.name


class Clothes(models.Model):
    PK_Clothes = models.AutoField(db_column='PK_Clothes', primary_key=True)
    name = models.CharField(
        db_column='name', max_length=100, verbose_name='Наименование')
    PK_Category = models.ForeignKey(
        Category, models.DO_NOTHING, db_column='PK_Category', verbose_name='Категория')
    PK_MainCategory = models.ForeignKey(
        MainCategory, models.DO_NOTHING, db_column='PK_MainCategory', verbose_name='Главная категория')
    PK_SubCategory = models.ForeignKey(
        SubCategory, models.DO_NOTHING, db_column='PK_SubCategory', verbose_name='Подкатегория')
    PK_Size = models.ForeignKey(
        Size, models.DO_NOTHING, db_column='PK_Size', verbose_name='Размер')
    PK_Color = models.ForeignKey(
        Color, models.DO_NOTHING, db_column='PK_Color', verbose_name='Цвет')
    price = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name='Цена')
    imagePath = models.ImageField(
        db_column='imagePath', max_length=255, blank=True, null=True, verbose_name='Фото')
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание')

    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL", blank=True)

    def __str__(self):
        return 'Товар: {}; {}; {}; {}; {};'.format(self.name, self.PK_Category, self.PK_Size, self.PK_Color, self.price)

    def get_absolute_url(self):
        return reverse('single-product', kwargs={
            'slug_MainCat': self.PK_MainCategory.slug,
            'slug_SubCat': self.PK_SubCategory.slug,
            'slug_Cat': self.PK_Category.slug,
            'slug_Clothes': self.slug
        })

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name + " " +self.PK_Size.name + " " + self.PK_Color.name + " " + str(self.price)))
        super(Clothes, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Clothes'
        verbose_name_plural = 'Одежда'
        verbose_name = 'Одежда'


class Gender(models.Model):
    PK_Gender = models.AutoField(db_column='PK_Gender', primary_key=True)
    name = models.CharField(
        db_column='name', max_length=100, verbose_name='Наименование')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        db_table = 'Gender'
        verbose_name_plural = 'Гендеры'
        verbose_name = 'Гендер'


class Customer(models.Model):
    PK_Customer = models.AutoField(db_column='PK_Customer', primary_key=True)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')

    email = models.EmailField(
        db_column='email', max_length=254, null=True, blank=True, verbose_name='E-mail')
    phone = models.CharField(
        db_column='phone', max_length=100, null=True, blank=True, verbose_name='Телефон')
    name = models.CharField(db_column='name', max_length=100,
                            null=True, blank=True, verbose_name='Имя')
    surname = models.CharField(
        db_column='surname', max_length=100, null=True, blank=True, verbose_name='Фамилия')
    midname = models.CharField(
        db_column='midname', max_length=100, null=True, blank=True, verbose_name='Отчество')
    birthday = models.DateField(
        db_column='birthday', null=True, blank=True, verbose_name='Дата рождения')

    PK_Gender = models.ForeignKey(
        Gender, models.DO_NOTHING, db_column='PK_Gender', null=True, blank=True, verbose_name='Пол')

    def __str__(self):
        return '{} - {}'.format(self.email, self.name)

    class Meta:
        db_table = 'Customer'
        verbose_name_plural = 'Клиенты'
        verbose_name = 'Клиент'


class CartItem(models.Model):
    PK_CartItem = models.AutoField(db_column='PK_CartItem', primary_key=True)
    name = models.CharField(
        db_column='name', max_length=100, verbose_name='Наименование')
    PK_Size = models.ForeignKey(
        Size, models.DO_NOTHING, db_column='PK_Size', verbose_name='Размер')
    PK_Color = models.ForeignKey(
        Color, models.DO_NOTHING, db_column='PK_Color', verbose_name='Цвет')
    price = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name='Цена')
    imagePath = models.ImageField(
        db_column='imagePath', max_length=255, blank=True, null=True, verbose_name='Фото')

    def __str__(self):
        return 'Товар корзины: {}; {}; {}; {};'.format(self.name, self.PK_Size, self.PK_Color, self.price)

    class Meta:
        db_table = 'CartItem'
        verbose_name_plural = 'Товары корзины'
        verbose_name = 'Товар корзины'


class Cart(models.Model):
    PK_Cart = models.AutoField(db_column='PK_Cart', primary_key=True)
    items = models.ManyToManyField(
        CartItem, db_column='items', verbose_name='Товары')
    totalPrice = models.DecimalField(
        db_column='totalPrice', max_digits=15, decimal_places=2, default=0, verbose_name='Общая сумма')
    totalItems = models.PositiveIntegerField(
        db_column='totalItems', default=0, verbose_name='Количество товаров')

    def UpdateTotal(self):
        self.totalPrice = sum(item.price for item in self.items.all())
        self.totalItems = len(self.items.all())
        self.save()

    def __str__(self):
        return 'Корзина: {} товар(ов), цена: {}'.format(self.totalItems, self.totalPrice)

    class Meta:
        db_table = 'Cart'
        verbose_name_plural = 'Корзины'
        verbose_name = 'Корзина'


class Order(models.Model):
    PK_Order = models.AutoField(db_column='PK_Order', primary_key=True)

    nameCustomer = models.CharField(
        db_column='nameCustomer', max_length=255, verbose_name='Имя')
    phoneCustomer = models.CharField(
        db_column='phoneCustomer', max_length=100, verbose_name='Телефон')
    emailCustomer = models.EmailField(
        db_column='emailCustomer', max_length=254, verbose_name='E-mail')

    PK_Cart = models.ForeignKey(Cart, models.DO_NOTHING, db_column='PK_Cart',
                                null=True, blank=True, verbose_name='Корзина')

    PK_Customer = models.ForeignKey(
        Customer, models.DO_NOTHING, db_column='PK_Customer', null=True, blank=True, verbose_name='Покупатель')

    date = models.DateTimeField(db_column='date', verbose_name='Дата заказа')

    def __str__(self):
        return '{}; {}; {}'.format(self.nameCustomer, self.phoneCustomer, self.emailCustomer)

    class Meta:
        db_table = 'Order'
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

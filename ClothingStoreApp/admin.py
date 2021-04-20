from django.contrib import admin
from .models import Size, MainCategory, SubCategory, Category, Color, Clothes, Order, Cart, CartItem, Customer, Gender

class MainCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ClothesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

    #pass

# Register your models here.
admin.site.register(Size)
admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Color)
admin.site.register(Clothes, ClothesAdmin)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(Customer)
admin.site.register(Gender)


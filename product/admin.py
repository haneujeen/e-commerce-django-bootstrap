from django.contrib import admin
from .models import Product, Company, Category, Tag, AdditionalFeature, Review, Cart, CartItem
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
admin.site.register(Product, MarkdownxModelAdmin)

class CompanyAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Company, CompanyAdmin)

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Tag, TagAdmin)

class AdditionalFeatureAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(AdditionalFeature, AdditionalFeatureAdmin)

admin.site.register(Review)

admin.site.register(Cart)

admin.site.register(CartItem)
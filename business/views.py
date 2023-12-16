from django.shortcuts import render
from product.models import Product, Category, Company

# Create your views here.
def landing(request):
  new_products = Product.objects.order_by('-pk')[:3]
  return render(request, 'business/landing.html', {
    'new_products': new_products,
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count(),
    'companies': Company.objects.all()
  })


def general(request):
  product = Product.objects.all()
  categories = Category.objects.all()
  category_table = Category.objects.all()[:3]
  company = Company.objects.all()
  company_table = Company.objects.all()[:3]
  return render(request, 'business/general.html', {
    'product': product,
    'categories': categories,
    'category_table': category_table,
    'company': company,
    'company_table': company_table
  })
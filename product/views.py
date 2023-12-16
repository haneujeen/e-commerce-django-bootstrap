from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Company, Tag, Review, Cart, CartItem
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import ReviewForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import productSerializer

class productViewSet(viewsets.ModelViewSet):
  queryset = Product.objects.all()
  serializer_class = productSerializer

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['product_image', 'detail_image', 'title', 'hook_text', 'product_price',
              'on_sale_price', 'rating', 'company', 'additional_feature', 'category',
              'description', 'markdown_desc']

    template_name = 'product/product_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_authenticated and request.user == self.get_object().author:
            return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(ProductUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(';', ',')
            tags_list = tags_str.split(',')
            for new_tag in tags_list:
                new_tag = new_tag.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=new_tag)
                if is_tag_created:
                    tag.slug = slugify(tag, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for tag in self.object.tags.all():
                tags_str_list.append(tag.name)
            context['tags_str_default'] = ';'.join(tags_str_list)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Product.objects.filter(category=None).count
        return context

class ProductCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Product
  fields = ['date', 'product_image', 'detail_image', 'title', 'hook_text', 'product_price',
            'on_sale_price', 'rating', 'company', 'additional_feature', 'category',
            'description', 'markdown_desc']

  def test_func(self):
      return self.request.user.is_superuser or self.request.user.is_staff

  def form_valid(self, form):
      current_user = self.request.user
      if current_user.is_authenticated and (current_user.is_superuser
                                            or current_user.is_staff):
          form.instance.author = current_user
          response = super(ProductCreate, self).form_valid(form)

          tags_str = self.request.POST.get('tags_str')
          if tags_str:
              tags_str = tags_str.strip()
              tags_str = tags_str.replace(';', ',')
              tags_list = tags_str.split(',')
              for new_tag in tags_list:
                  new_tag = new_tag.strip()
                  tag, is_tag_created = Tag.objects.get_or_create(name=new_tag)
                  if is_tag_created:
                      tag.slug = slugify(tag, allow_unicode=True)
                      tag.save()
                  self.object.tags.add(tag)
          return response
      else:
          return redirect('/product/')

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(ProductCreate, self).get_context_data()
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Product.objects.filter(category=None).count()
    return context

class ProductDetail(DetailView):
  model = Product

  def get_context_data(self, **kwargs):
    context = super(ProductDetail, self).get_context_data()
    context['related_products'] = Product.objects.filter(category_id=self.object.category_id).order_by('-pk')[0:4]
    context['related_products_count'] = Product.objects.filter(category_id=self.object.category_id).count()-1
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Product.objects.filter(category=None).count()
    context['companies'] = Company.objects.all()
    context['review_form'] = ReviewForm
    return context

class ProductList(ListView):
  model = Product
  paginate_by = 8

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(ProductList, self).get_context_data()
    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Product.objects.filter(category=None).count
    context['companies'] = Company.objects.all()
    return context

class CartList(LoginRequiredMixin, ListView):
  model = Cart

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(CartList, self).get_context_data()
    cart = Cart.objects.get(user=self.request.user)
    context['cart'] = cart
    context['items'] = CartItem.objects.filter(cart=cart)
    context['items_set_count'] = CartItem.objects.filter(cart=cart).count()
    context['companies'] = Company.objects.all()
    return context

class ProductSearch(ProductList):
    pagenated_by = None
    ordering = '-pk'

    def get_queryset(self):
        q = self.kwargs['q']
        product_list = Product.objects.filter(
            Q(title__contains = q) | Q(description__contains = q) | Q(tags__name__contains = q)
        ).distinct()
        return product_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductSearch, self).get_context_data()
        q = self.kwargs['q']
        context['q'] = self.kwargs['q']
        context['search_info'] = f'{q}와 관련된 상품은 {self.get_queryset().count()}개입니다.'
        return context

def about_page(request):
  frame_list = ['django', 'bootstrap4.5', 'django-rest']
  lib_list = ['crispy forms', 'allauth']
  return render(request, 'product/about.html', {
    'frame_list': frame_list,
    'lib_list': lib_list,
    'product_list': Product.objects.all()[0:7],
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count(),
    'companies': Company.objects.all()
  })

def new_items_page(request):
  new_items = Product.objects.all().order_by('-pk')[0:4]
  return render(request, 'product/product_list.html', {
    'new_items': new_items,
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count()
  })

def popular_items_page(request):
  popular_items = Product.objects.filter(rating=5).order_by('-pk')
  return render(request, 'product/product_list.html', {
    'popular_items': popular_items,
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count(),
    'companies': Company.objects.all()
  })

def category_page(request, slug):
  if slug == 'no_category':
    category = 'etc'
    product_list = Product.objects.filter(category=None).order_by('-pk')
  else:
    category = Category.objects.get(slug=slug)
    product_list = Product.objects.filter(category=category).order_by('-pk')
  return render(request, 'product/product_list.html', {
    'category': category,
    'product_list': product_list,
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count(),
    'companies': Company.objects.all()
  })

def company_page(request, slug):
  company = Company.objects.get(slug=slug)
  product_list = Product.objects.filter(company=company).order_by('-pk')

  page_number = request.GET.get('page', 1)
  paginator = Paginator(product_list, 4)

  page_obj = paginator.get_page(page_number)

  return render(request, 'product/product_list.html', {
    'company': company,
    'product_list': product_list,
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count(),
    'companies': Company.objects.all(),
    'page_obj': page_obj
  })

def tag_page(request, slug):
  tag = Tag.objects.get(slug=slug)
  product_list = tag.product_set.all().filter(tags=tag).order_by('-pk')
  return render(request, 'product/product_list.html', {
    'tag': tag,
    'product_list': product_list,
    'no_tag_product_count': Product.objects.filter(tags=None).count,
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count(),
  })

def new_review(request, pk):
  if request.user.is_authenticated:
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
      review_form = ReviewForm(request.POST)
      if review_form.is_valid():
        review = review_form.save(commit=False)
        review.product = product
        review.writer = request.user
        review.save()
        return redirect(review.get_absolute_url())
    else:
      return redirect(product.get_absolute_url())
  else:
    raise PermissionDenied

def new_child_comment(request, pk, review_pk):
  if request.user.is_authenticated:
    product = get_object_or_404(Product, pk=pk)
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
      form = request.POST.get('childComment-form')
      content = request.POST.get('commentContent')
      child_comment = Review.objects.create(product = product, content = content, writer=request.user)
      child_comment.parent_review = review
      child_comment.save()
      return redirect(review.get_absolute_url())
    else:
      return redirect(product.get_absolute_url())
  else:
    raise PermissionDenied

def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    product = review.product

    if request.user.is_authenticated and request.user == review.writer:
      review.delete()
    else:
      raise PermissionDenied
    return redirect(product.get_absolute_url())

class ReviewUpdate(LoginRequiredMixin, UpdateView):
  model = Review
  form_class = ReviewForm

  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated and request.user == self.get_object().writer:
      return super(ReviewUpdate, self).dispatch(request, *args, **kwargs)
    else:
      raise PermissionDenied

def product_list_page(request):
  return render(request, 'product/base.html', {
    'product_edit_list': Product.objects.all(),
    'categories': Category.objects.all(),
    'no_category_post_count': Product.objects.filter(category=None).count(),
    'companies': Company.objects.all(),
  })

@login_required
def add_cart(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            product = get_object_or_404(Product, pk=pk)
            cart, is_cart_created = Cart.objects.get_or_create(user=request.user)
            cart_item, is_cart_item_created = CartItem.objects.get_or_create(item=product)
            quantity = request.POST.get('inputQuantity')
            if is_cart_item_created:
                # 카트아이템이 없으면
                if quantity:
                    cart_item.cart = cart
                    cart_item.qty = quantity
                    cart_item.save()
                else:
                    cart_item.cart = cart
                    cart_item.qty = 1
                    cart_item.save()
            else:
                cart_item.cart = cart
                if quantity:
                    cart_item.qty += int(quantity)
                    cart_item.save()
                else:
                    cart_item.qty += 1
                    cart_item.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
          return redirect('/product/')
    else:
      return redirect ('/product/')

@login_required
def remove_cart(request, pk):
  cart = Cart.objects.get(user=request.user)
  product = get_object_or_404(Product, pk=pk)
  cart_item = cart.cartitem_set.get(item=product)
  cart_item.delete()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def user_page(request, user):
  if request.user.is_authenticated:
    user = request.user
    return render(request, 'product/my_page.html', {
      'user': user,
      'product_list': Product.objects.all()[0:7],
      'categories': Category.objects.all(),
      'no_category_post_count': Product.objects.filter(category=None).count(),
      'companies': Company.objects.all()
    })
  else:
    raise PermissionDenied


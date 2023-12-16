from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F, Sum
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdown, markdownify


# Create your models here.



class AdditionalFeature(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name

class Tag(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f'/product/tag/{self.slug}/'

class Category(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f'/product/category/{self.slug}/'

  class Meta:
    verbose_name_plural = 'Categories'

class Company(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
  address = models.CharField(max_length=70)
  contact = models.CharField(max_length=50, unique=True)
  company_image = models.ImageField(upload_to='product/company/images/%Y/%m/%d/', blank=True)
  description = models.CharField(max_length=255, blank=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f'/product/company/{self.slug}/'

  class Meta:
    verbose_name_plural = 'Companies'

class Product(models.Model):
    title = models.CharField(max_length=80)
    hook_text = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    markdown_desc = MarkdownxField(blank=True)
    date = models.DateField(default=timezone.now, editable=True)
    product_image = models.ImageField(upload_to='product/product/images//%Y/%m/%d/', blank=True)
    detail_image = models.ImageField(upload_to='product/product/images/%Y/%m/%d/', blank=True)
    product_price = models.IntegerField(default=0)
    on_sale_price = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    additional_feature = models.ForeignKey(AdditionalFeature, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, default='admin', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}] {self.title}:: {self.product_price} : {self.company}'

    def get_absolute_url(self):
        return f'/product/{self.pk}/'

    def get_content_markdown(self):
        return markdownify(self.markdown_desc)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    parent_review = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.writer}: {self.content}'

    def get_absolute_url(self):
        return f'{self.product.get_absolute_url()}#review_anchor_{self.pk}'

    def get_avatar_url(self):
        if self.writer.socialaccount_set.exists():
            return self.writer.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
      return f'/product/cart/{self.user.id}'

    @property
    def total_price(self):
      return self.cartitem_set.aggregate(price=Sum(
        F('item__product_price') *
        F('qty'),
        output_field=models.IntegerField()
      ))

class CartItem(models.Model):
  item = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
  qty = models.IntegerField(default=0)
  cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.cart.user}의 카트: {self.item} {self.qty}개'

  @property
  def total_price(self):
    return int(self.qty * self.item.product_price)


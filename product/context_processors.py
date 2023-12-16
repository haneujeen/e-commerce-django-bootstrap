

def my_cart(request):
  from product.models import Cart, CartItem
  if request.user.is_authenticated:
      cart, is_created = Cart.objects.get_or_create(user=request.user)
      if cart:
        items_set_count = CartItem.objects.filter(cart=cart).count()
        total_price = cart.total_price
        return {
          'items_set_count': items_set_count,
          'total_price': total_price,
        }
      else:
        return {
          'items_set_count': '0'
        }
  else:
    return {
      'items_set_count': '0'
    }

def category(request):
  from product.models import Product, Category

  return {
    'categories': Category.objects.all(),
  }


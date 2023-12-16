from django.urls import path
from . import views

urlpatterns=[
    path('', views.ProductList.as_view()),
    path('<int:pk>/', views.ProductDetail.as_view()),
    path('<int:pk>/new_review/', views.new_review),
    path('<int:pk>/<int:review_pk>/new_child_comment/', views.new_child_comment),
    path('create_product/', views.ProductCreate.as_view()),
    path('update_product/<int:pk>/', views.ProductUpdate.as_view()),
    path('edit_review/<int:pk>/', views.ReviewUpdate.as_view()),
    path('delete_review/<int:pk>/', views.delete_review),
    path('category/<str:slug>/', views.category_page),
    path('company/<str:slug>/', views.company_page),
    path('popular_items/', views.popular_items_page),
    path('tag/<str:slug>/', views.tag_page),
    path('new_arrivals/', views.new_items_page),
    path('about/', views.about_page),
    path('search/<str:q>/', views.ProductSearch.as_view()),
    path('update_product/list/', views.product_list_page),
    path('cart/<str:user>/', views.CartList.as_view()),
    path('cart/add/<int:pk>/', views.add_cart),
    path('cart/remove/<int:pk>', views.remove_cart, name='removeItem'),
    path('user/<str:user>/', views.user_page),
]
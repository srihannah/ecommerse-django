from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('cart',views.cart_page,name='cart'),
    path('fav',views.fav_page,name='fav'),
    path('favviewpage',views.favviewpage,name='favviewpage'),
    path('remove_cart/<str:cid>',views.remove_cart,name='remove_cart'),
    path('remove_fav/<str:fid>',views.remove_fav,name='remove_fav'),
    path('checkout/<int:product_id>/',views.checkout,name='checkout'),
    path('checkout_home/<int:product_id>/', views.checkout_home, name='checkout_home'),
    path('register',views.register,name='register'),
    path('collection',views.collection,name='collection'),
    path('collection/<str:name>',views.collectionview,name='collection'),
    path('collection/<str:cname>/<str:pname>',views.product_details,name='product_details'),
    path('addtocart',views.add_to_cart,name='addtocart'),
    # Add a URL for the order success page
    path('order-success',views.order_success, name='order_success'),
    
]

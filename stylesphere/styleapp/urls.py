from django.urls import path
from .import views
from django.contrib import admin

urlpatterns = [
   path('',views.index,name='index'),
   path('signin',views.signin,name='signin'),
   path('signup',views.signup,name='signup'),
   path('about',views.about,name='about'),
   path('categorypage',views.categorypage,name='categorypage'),
   path('categoryviewpage/<int:a>',views.categoryviewpage,name='categoryviewpage'),
   path('viewmorepage/<int:a>',views.viewmorepage,name='viewmorepage'),
   path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
   path('delete_cart/<int:a>',views.delete_cart,name='delete_cart'),
   path('cart_view/', views.cart_view, name='cart_view'),
   path('logout_user',views.logout_user,name='logout_user'),
]  


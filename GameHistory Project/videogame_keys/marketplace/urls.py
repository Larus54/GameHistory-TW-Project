from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:listing_id>/add_review/', views.add_review, name='add_review'),
    path('delete_listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    path('buy_listing/<int:listing_id>/', views.buy_listing, name='buy_listing'),
    path('add_quantity/<int:listing_id>/', views.add_quantity, name='add_quantity'),
    path('registration/signup/', views.signup, name='signup'),
    path('create/', views.create_listing, name='create_listing'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path('profile/', views.user_profile, name='user_profile'),
    path("user_purchases/", views.user_purchases, name="user_purchases"),
    path('search/', views.search_listings, name='search_listings'),
    path('listing/<int:listing_id>/offer/', views.create_offer, name='create_offer'),
    path('manage_offers/', views.manage_offers, name='manage_offers'),
    path('offer/<int:offer_id>/<str:response>/', views.respond_to_offer, name='respond_to_offer'),
    path('listing/<int:listing_id>/modify', views.edit_listing, name='edit_listing'),
]
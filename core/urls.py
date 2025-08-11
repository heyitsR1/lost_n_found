from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_us, name='contact'),
    
    # Item CRUD
    path('item/new/', views.item_create, name='item_create'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/<int:pk>/edit/', views.item_update, name='item_update'),
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),
    
    # User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Search
    path('search/', views.search_items, name='search_items'),
] 
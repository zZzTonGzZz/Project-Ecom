from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('search/', views.search, name='search'),
    path('add_item/', views.add_item, name='add_item'),
    path('confirm_delete/<str:pk>', views.confirm_delete, name='confirm_delete'),
    path('product/<int:pk>/update/', views.product_update, name='product_update'),
    path('add_category/', views.add_category, name='add_category'),
    
    # Sales Report and Order Management URLs
    path('sales-report/', views.sales_report, name='sales_report'),
    path('order-management/', views.order_management, name='order_management'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('bulk-order-actions/', views.bulk_order_actions, name='bulk_order_actions'),
    path('api/sales-report/', views.sales_report_api, name='sales_report_api'),
    
    # Customer Order Tracking URLs
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order-tracking/<int:order_id>/', views.order_tracking, name='order_tracking'),
    path('order-lookup/', views.order_lookup, name='order_lookup'),
]

from django.urls import path
from . import views

urlpatterns = [
    # 认证相关
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
    path('change-password/', views.change_password, name='change_password'),
    
    # 主页
    path('', views.index, name='index'),
    
    # 产品分类管理
    path('product-categories/', views.product_category_list, name='product_category_list'),
    path('product-categories/create/', views.product_category_create, name='product_category_create'),
    path('product-categories/<int:pk>/update/', views.product_category_update, name='product_category_update'),
    path('product-categories/<int:pk>/delete/', views.product_category_delete, name='product_category_delete'),
    
    # 产品管理
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # 订单管理
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/update/', views.order_update, name='order_update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('orders/<int:order_pk>/items/add/', views.order_item_add, name='order_item_add'),
    path('orders/items/<int:pk>/update/', views.order_item_update, name='order_item_update'),
    path('orders/items/<int:pk>/delete/', views.order_item_delete, name='order_item_delete'),
    
    # 物流追踪管理
    path('logistics/', views.logistics_list, name='logistics_list'),
    path('logistics/create/', views.logistics_create, name='logistics_create'),
    path('logistics/<int:pk>/', views.logistics_detail, name='logistics_detail'),
    path('logistics/<int:pk>/update/', views.logistics_update, name='logistics_update'),
    path('logistics/<int:pk>/delete/', views.logistics_delete, name='logistics_delete'),
    path('logistics/<int:logistics_pk>/records/add/', views.tracking_record_add, name='tracking_record_add'),
    path('logistics/records/<int:pk>/update/', views.tracking_record_update, name='tracking_record_update'),
    path('logistics/records/<int:pk>/delete/', views.tracking_record_delete, name='tracking_record_delete'),
    
    # 报表统计
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/inventory/', views.inventory_report, name='inventory_report'),
    path('reports/logistics/', views.logistics_report, name='logistics_report'),
    
    # 出货管理
    path('shipments/', views.shipment_list, name='shipment_list'),
    path('shipments/<int:pk>/', views.shipment_detail, name='shipment_detail'),
    path('shipments/create/', views.shipment_create, name='shipment_create'),
    path('shipments/<int:pk>/update/', views.shipment_update, name='shipment_update'),
    path('shipments/<int:pk>/delete/', views.shipment_delete, name='shipment_delete'),
    
    # 进货管理
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('purchases/<int:pk>/', views.purchase_detail, name='purchase_detail'),
    path('purchases/create/', views.purchase_create, name='purchase_create'),
    path('purchases/<int:pk>/update/', views.purchase_update, name='purchase_update'),
    path('purchases/<int:pk>/delete/', views.purchase_delete, name='purchase_delete'),
]
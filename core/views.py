from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Shipment, Purchase, ProductCategory, Product, Order, OrderItem, LogisticsTracking, TrackingRecord
from .forms import ShipmentForm, PurchaseForm, PasswordChangeForm, ProductCategoryForm, ProductForm, OrderForm, OrderItemForm


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, '登录成功！')
            return redirect('index')
        else:
            messages.error(request, '用户名或密码错误，请重试。')
    
    return render(request, 'core/login.html')


def user_register(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST.get('email', '')
        
        if password1 != password2:
            messages.error(request, '两次输入的密码不一致！')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在！')
            return redirect('register')
        
        # 创建新用户
        user = User.objects.create_user(
            username=username,
            password=password1,
            email=email
        )
        
        messages.success(request, '注册成功！请登录。')
        return redirect('login')
    
    return render(request, 'core/register.html')


@login_required
def user_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, '个人资料更新成功！')
        return redirect('user_profile')
    
    return render(request, 'core/user_profile.html', {'user': request.user})


def user_logout(request):
    logout(request)
    messages.success(request, '已成功退出登录！')
    return redirect('login')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            
            # 验证旧密码
            user = authenticate(request, username=request.user.username, password=old_password)
            if user is not None:
                # 更新密码
                user.set_password(new_password)
                user.save()
                messages.success(request, '密码修改成功！请重新登录。')
                return redirect('login')
            else:
                messages.error(request, '旧密码错误，请重试。')
    else:
        form = PasswordChangeForm()
    
    return render(request, 'core/change_password.html', {'form': form})


# 产品分类管理视图
@login_required
def product_category_list(request):
    query = request.GET.get('q', '')
    categories = ProductCategory.objects.all()
    
    if query:
        categories = categories.filter(name__icontains=query)
    
    return render(request, 'core/product_category_list.html', {'categories': categories, 'query': query})


@login_required
def product_category_create(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, '产品分类创建成功！')
            return redirect('product_category_list')
    else:
        form = ProductCategoryForm()
    
    return render(request, 'core/product_category_form.html', {'form': form, 'title': '创建产品分类'})


@login_required
def product_category_update(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, '产品分类更新成功！')
            return redirect('product_category_list')
    else:
        form = ProductCategoryForm(instance=category)
    
    return render(request, 'core/product_category_form.html', {'form': form, 'title': '编辑产品分类'})


@login_required
def product_category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    category.delete()
    messages.success(request, '产品分类删除成功！')
    return redirect('product_category_list')


# 产品管理视图
@login_required
def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(model__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    return render(request, 'core/product_list.html', {'products': products, 'query': query})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, '产品创建成功！')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'core/product_form.html', {'form': form, 'title': '创建产品'})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '产品更新成功！')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'core/product_form.html', {'form': form, 'title': '编辑产品'})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, '产品删除成功！')
    return redirect('product_list')


# 订单管理视图
@login_required
def order_list(request):
    query = request.GET.get('q', '')
    orders = Order.objects.all()
    
    if query:
        orders = orders.filter(
            Q(order_number__icontains=query) |
            Q(customer_name__icontains=query) |
            Q(customer_contact__icontains=query)
        )
    
    return render(request, 'core/order_list.html', {'orders': orders, 'query': query})


@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            messages.success(request, '订单创建成功！')
            return redirect('order_list')
    else:
        form = OrderForm()
    
    return render(request, 'core/order_form.html', {'form': form, 'title': '创建订单'})


@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, '订单更新成功！')
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    
    return render(request, 'core/order_form.html', {'form': form, 'title': '编辑订单'})


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    messages.success(request, '订单删除成功！')
    return redirect('order_list')


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = order.items.all()
    return render(request, 'core/order_detail.html', {'order': order, 'order_items': order_items})


@login_required
def order_item_add(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            # 更新订单总金额
            order.total_amount = sum(item.subtotal for item in order.items.all())
            order.save()
            messages.success(request, '订单商品添加成功！')
            return redirect('order_detail', pk=order_pk)
    else:
        form = OrderItemForm()
    
    return render(request, 'core/order_item_form.html', {'form': form, 'title': '添加订单商品', 'order': order})


@login_required
def order_item_update(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    order = order_item.order
    
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=order_item)
        if form.is_valid():
            form.save()
            # 更新订单总金额
            order.total_amount = sum(item.subtotal for item in order.items.all())
            order.save()
            messages.success(request, '订单商品更新成功！')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderItemForm(instance=order_item)
    
    return render(request, 'core/order_item_form.html', {'form': form, 'title': '编辑订单商品', 'order': order})


@login_required
def order_item_delete(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    order = order_item.order
    order_item.delete()
    # 更新订单总金额
    order.total_amount = sum(item.subtotal for item in order.items.all())
    order.save()
    messages.success(request, '订单商品删除成功！')
    return redirect('order_detail', pk=order.pk)


# 物流追踪管理视图
@login_required
def logistics_list(request):
    query = request.GET.get('q', '')
    logistics = LogisticsTracking.objects.all()
    
    if query:
        logistics = logistics.filter(
            Q(tracking_number__icontains=query) |
            Q(carrier__icontains=query) |
            Q(order__order_number__icontains=query)
        )
    
    return render(request, 'core/logistics_list.html', {'logistics': logistics, 'query': query})


@login_required
def logistics_create(request):
    if request.method == 'POST':
        form = LogisticsTrackingForm(request.POST)
        if form.is_valid():
            logistics = form.save(commit=False)
            logistics.created_by = request.user
            logistics.save()
            messages.success(request, '物流追踪创建成功！')
            return redirect('logistics_list')
    else:
        form = LogisticsTrackingForm()
    
    return render(request, 'core/logistics_form.html', {'form': form, 'title': '创建物流追踪'})


@login_required
def logistics_update(request, pk):
    logistics = get_object_or_404(LogisticsTracking, pk=pk)
    
    if request.method == 'POST':
        form = LogisticsTrackingForm(request.POST, instance=logistics)
        if form.is_valid():
            form.save()
            messages.success(request, '物流追踪更新成功！')
            return redirect('logistics_list')
    else:
        form = LogisticsTrackingForm(instance=logistics)
    
    return render(request, 'core/logistics_form.html', {'form': form, 'title': '编辑物流追踪'})


@login_required
def logistics_delete(request, pk):
    logistics = get_object_or_404(LogisticsTracking, pk=pk)
    logistics.delete()
    messages.success(request, '物流追踪删除成功！')
    return redirect('logistics_list')


@login_required
def logistics_detail(request, pk):
    logistics = get_object_or_404(LogisticsTracking, pk=pk)
    tracking_records = logistics.records.all()
    return render(request, 'core/logistics_detail.html', {'logistics': logistics, 'tracking_records': tracking_records})


@login_required
def tracking_record_add(request, logistics_pk):
    logistics = get_object_or_404(LogisticsTracking, pk=logistics_pk)
    
    if request.method == 'POST':
        form = TrackingRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.tracking = logistics
            record.save()
            # 更新物流状态
            logistics.status = record.status
            logistics.save()
            messages.success(request, '物流轨迹记录添加成功！')
            return redirect('logistics_detail', pk=logistics_pk)
    else:
        form = TrackingRecordForm(initial={'tracking': logistics})
    
    return render(request, 'core/tracking_record_form.html', {'form': form, 'title': '添加物流轨迹记录', 'logistics': logistics})


@login_required
def tracking_record_update(request, pk):
    record = get_object_or_404(TrackingRecord, pk=pk)
    logistics = record.tracking
    
    if request.method == 'POST':
        form = TrackingRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            # 更新物流状态
            logistics.status = record.status
            logistics.save()
            messages.success(request, '物流轨迹记录更新成功！')
            return redirect('logistics_detail', pk=logistics.pk)
    else:
        form = TrackingRecordForm(instance=record)
    
    return render(request, 'core/tracking_record_form.html', {'form': form, 'title': '编辑物流轨迹记录', 'logistics': logistics})


@login_required
def tracking_record_delete(request, pk):
    record = get_object_or_404(TrackingRecord, pk=pk)
    logistics = record.tracking
    record.delete()
    # 更新物流状态为最新记录的状态
    latest_record = logistics.records.first()
    if latest_record:
        logistics.status = latest_record.status
        logistics.save()
    messages.success(request, '物流轨迹记录删除成功！')
    return redirect('logistics_detail', pk=logistics.pk)


# 报表统计视图
@login_required
def sales_report(request):
    # 统计销售数据
    from django.db.models import Sum, Count
    from django.utils import timezone
    
    # 总销售额
    total_sales = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    
    # 订单数量
    order_count = Order.objects.count()
    
    # 按状态统计订单
    order_status_counts = Order.objects.values('status').annotate(count=Count('id'))
    
    # 最近30天的销售趋势
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    daily_sales = Order.objects.filter(
        created_at__gte=thirty_days_ago
    ).values('created_at__date').annotate(
        sales=Sum('total_amount'),
        orders=Count('id')
    ).order_by('created_at__date')
    
    context = {
        'total_sales': total_sales,
        'order_count': order_count,
        'order_status_counts': order_status_counts,
        'daily_sales': daily_sales,
    }
    
    return render(request, 'core/sales_report.html', context)


@login_required
def inventory_report(request):
    # 统计库存数据
    from django.db.models import Sum, F
    
    # 总库存数量
    total_stock = Product.objects.aggregate(total=Sum('stock'))['total'] or 0
    
    # 总库存价值
    total_value = Product.objects.aggregate(
        total=Sum(F('stock') * F('price'))
    )['total'] or 0
    
    # 库存不足的产品（库存小于10）
    low_stock_products = Product.objects.filter(stock__lt=10)
    
    # 按分类统计库存
    category_stock = Product.objects.values('category__name').annotate(
        total_stock=Sum('stock'),
        total_value=Sum(F('stock') * F('price'))
    ).filter(category__isnull=False)
    
    context = {
        'total_stock': total_stock,
        'total_value': total_value,
        'low_stock_products': low_stock_products,
        'category_stock': category_stock,
    }
    
    return render(request, 'core/inventory_report.html', context)


@login_required
def logistics_report(request):
    # 统计物流数据
    from django.db.models import Count, Avg
    from django.utils import timezone
    
    # 总物流单数量
    total_logistics = LogisticsTracking.objects.count()
    
    # 按状态统计物流单
    logistics_status_counts = LogisticsTracking.objects.values('status').annotate(count=Count('id'))
    
    # 最近30天的物流单趋势
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    daily_logistics = LogisticsTracking.objects.filter(
        created_at__gte=thirty_days_ago
    ).values('created_at__date').annotate(
        count=Count('id')
    ).order_by('created_at__date')
    
    context = {
        'total_logistics': total_logistics,
        'logistics_status_counts': logistics_status_counts,
        'daily_logistics': daily_logistics,
    }
    
    return render(request, 'core/logistics_report.html', context)


@login_required
def index(request):
    # 统计数据
    today = timezone.now().date()
    this_month = today.replace(day=1)
    
    shipment_count = Shipment.objects.count()
    purchase_count = Purchase.objects.count()
    
    recent_shipments = Shipment.objects.order_by('-created_at')[:5]
    recent_purchases = Purchase.objects.order_by('-created_at')[:5]
    
    context = {
        'shipment_count': shipment_count,
        'purchase_count': purchase_count,
        'recent_shipments': recent_shipments,
        'recent_purchases': recent_purchases,
    }
    
    return render(request, 'core/index.html', context)


# 出货管理视图
@login_required
def shipment_list(request):
    query = request.GET.get('q', '')
    shipments = Shipment.objects.all()
    
    if query:
        shipments = shipments.filter(
            Q(goods_name__icontains=query) |
            Q(region__icontains=query) |
            Q(ship_date__icontains=query)
        )
    
    return render(request, 'core/shipment_list.html', {'shipments': shipments, 'query': query})


@login_required
def shipment_detail(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    return render(request, 'core/shipment_detail.html', {'shipment': shipment})


@login_required
def shipment_create(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.created_by = request.user
            shipment.save()
            messages.success(request, '出货记录创建成功！')
            return redirect('shipment_list')
    else:
        form = ShipmentForm()
    
    return render(request, 'core/shipment_form.html', {'form': form, 'title': '创建出货记录'})


@login_required
def shipment_update(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            messages.success(request, '出货记录更新成功！')
            return redirect('shipment_list')
    else:
        form = ShipmentForm(instance=shipment)
    
    return render(request, 'core/shipment_form.html', {'form': form, 'title': '编辑出货记录'})


@login_required
def shipment_delete(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    shipment.delete()
    messages.success(request, '出货记录删除成功！')
    return redirect('shipment_list')


# 进货管理视图
@login_required
def purchase_list(request):
    query = request.GET.get('q', '')
    purchases = Purchase.objects.all()
    
    if query:
        purchases = purchases.filter(
            Q(goods_name__icontains=query) |
            Q(supplier_name__icontains=query) |
            Q(purchase_date__icontains=query)
        )
    
    return render(request, 'core/purchase_list.html', {'purchases': purchases, 'query': query})


@login_required
def purchase_detail(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    return render(request, 'core/purchase_detail.html', {'purchase': purchase})


@login_required
def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.created_by = request.user
            purchase.save()
            messages.success(request, '进货记录创建成功！')
            return redirect('purchase_list')
    else:
        form = PurchaseForm()
    
    return render(request, 'core/purchase_form.html', {'form': form, 'title': '创建进货记录'})


@login_required
def purchase_update(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            messages.success(request, '进货记录更新成功！')
            return redirect('purchase_list')
    else:
        form = PurchaseForm(instance=purchase)
    
    return render(request, 'core/purchase_form.html', {'form': form, 'title': '编辑进货记录'})


@login_required
def purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    purchase.delete()
    messages.success(request, '进货记录删除成功！')
    return redirect('purchase_list')

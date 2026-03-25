from django.db import models
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    # 产品分类模型
    name = models.CharField(max_length=100, verbose_name='分类名称')
    description = models.TextField(blank=True, null=True, verbose_name='分类描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '产品分类'
        verbose_name_plural = '产品分类'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    # 产品模型
    name = models.CharField(max_length=200, verbose_name='产品名称')
    model = models.CharField(max_length=100, verbose_name='产品型号')
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, verbose_name='产品分类')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    stock = models.IntegerField(verbose_name='库存数量')
    description = models.TextField(blank=True, null=True, verbose_name='产品描述')
    image_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='产品图片')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.model})"


class Order(models.Model):
    # 订单模型
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('paid', '已付款'),
        ('shipped', '已发货'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True, verbose_name='订单号')
    customer_name = models.CharField(max_length=100, verbose_name='客户姓名')
    customer_contact = models.CharField(max_length=20, verbose_name='客户联系方式')
    customer_address = models.TextField(verbose_name='客户地址')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='订单总金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ['-created_at']

    def __str__(self):
        return f"订单 {self.order_number} - {self.customer_name}"


class OrderItem(models.Model):
    # 订单商品模型
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='产品')
    product_name = models.CharField(max_length=200, verbose_name='产品名称')
    product_model = models.CharField(max_length=100, verbose_name='产品型号')
    quantity = models.IntegerField(verbose_name='数量')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='小计')

    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = '订单商品'

    def __str__(self):
        return f"{self.product_name} - {self.quantity}件"

    def save(self, *args, **kwargs):
        # 自动计算小计
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class Shipment(models.Model):
    # 出货信息字段
    STATUS_CHOICES = [
        ('shipped', '已发货'),
        ('received', '已签收'),
        ('exception', '异常'),
    ]
    
    goods_name = models.CharField(max_length=100, verbose_name='货物名称')
    model = models.CharField(max_length=100, verbose_name='出货型号')
    ship_date = models.DateField(verbose_name='出货日期')
    region = models.CharField(max_length=100, verbose_name='出货地区')
    warehouse = models.CharField(max_length=100, verbose_name='出货仓库')
    shipper = models.CharField(max_length=100, verbose_name='出货人')
    receiver = models.CharField(max_length=100, verbose_name='收货人')
    contact = models.CharField(max_length=20, verbose_name='联系方式')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    quantity = models.IntegerField(verbose_name='出货数量')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='出货总价')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='shipped', verbose_name='出货状态')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '出货记录'
        verbose_name_plural = '出货记录'
        ordering = ['-ship_date', '-created_at']

    def __str__(self):
        return f"{self.goods_name} - {self.ship_date}"

    def save(self, *args, **kwargs):
        # 自动计算总价
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class Purchase(models.Model):
    # 进货信息字段
    STATUS_CHOICES = [
        ('in_stock', '已入库'),
        ('pending', '待入库'),
    ]
    
    goods_name = models.CharField(max_length=100, verbose_name='货物名称')
    model = models.CharField(max_length=100, verbose_name='进货型号')
    purchase_date = models.DateField(verbose_name='进货日期')
    supplier_name = models.CharField(max_length=100, verbose_name='供应商名称')
    supplier_contact = models.CharField(max_length=20, verbose_name='供应商联系方式')
    purchaser = models.CharField(max_length=100, verbose_name='进货人')
    receiver = models.CharField(max_length=100, verbose_name='收货人')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    quantity = models.IntegerField(verbose_name='进货数量')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='总价格')
    warehouse = models.CharField(max_length=100, verbose_name='入库仓库')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='入库状态')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '进货记录'
        verbose_name_plural = '进货记录'
        ordering = ['-purchase_date', '-created_at']

    def __str__(self):
        return f"{self.goods_name} - {self.purchase_date}"

    def save(self, *args, **kwargs):
        # 自动计算总价
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class LogisticsTracking(models.Model):
    # 物流追踪模型
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单')
    tracking_number = models.CharField(max_length=100, verbose_name='物流单号')
    carrier = models.CharField(max_length=100, verbose_name='物流公司')
    status = models.CharField(max_length=50, verbose_name='物流状态')
    estimated_delivery = models.DateField(blank=True, null=True, verbose_name='预计送达日期')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '物流追踪'
        verbose_name_plural = '物流追踪'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tracking_number} - {self.carrier}"


class TrackingRecord(models.Model):
    # 物流轨迹记录模型
    tracking = models.ForeignKey(LogisticsTracking, on_delete=models.CASCADE, related_name='records', verbose_name='物流追踪')
    timestamp = models.DateTimeField(verbose_name='时间')
    location = models.CharField(max_length=200, verbose_name='地点')
    status = models.CharField(max_length=100, verbose_name='状态描述')
    details = models.TextField(blank=True, null=True, verbose_name='详细信息')

    class Meta:
        verbose_name = '物流轨迹记录'
        verbose_name_plural = '物流轨迹记录'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.location} - {self.status}"

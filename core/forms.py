from django import forms
from .models import Shipment, Purchase, ProductCategory, Product, Order, OrderItem, LogisticsTracking, TrackingRecord

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'model', 'category', 'price', 'stock',
            'description', 'image_url'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = [
            'goods_name', 'model', 'ship_date', 'region', 'warehouse',
            'shipper', 'receiver', 'contact', 'unit_price', 'quantity',
            'status', 'remark'
        ]
        widgets = {
            'ship_date': forms.DateInput(attrs={'type': 'date'}),
            'remark': forms.Textarea(attrs={'rows': 3}),
        }


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = [
            'goods_name', 'model', 'purchase_date', 'supplier_name',
            'supplier_contact', 'purchaser', 'receiver', 'unit_price',
            'quantity', 'warehouse', 'status', 'remark'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'remark': forms.Textarea(attrs={'rows': 3}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'order_number', 'customer_name', 'customer_contact',
            'customer_address', 'total_amount', 'status', 'remark'
        ]
        widgets = {
            'customer_address': forms.Textarea(attrs={'rows': 3}),
            'remark': forms.Textarea(attrs={'rows': 3}),
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = [
            'product', 'product_name', 'product_model',
            'quantity', 'unit_price', 'subtotal'
        ]


class LogisticsTrackingForm(forms.ModelForm):
    class Meta:
        model = LogisticsTracking
        fields = [
            'order', 'tracking_number', 'carrier',
            'status', 'estimated_delivery'
        ]
        widgets = {
            'estimated_delivery': forms.DateInput(attrs={'type': 'date'}),
        }


class TrackingRecordForm(forms.ModelForm):
    class Meta:
        model = TrackingRecord
        fields = [
            'tracking', 'timestamp', 'location',
            'status', 'details'
        ]
        widgets = {
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'details': forms.Textarea(attrs={'rows': 3}),
        }


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='旧密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='新密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='确认新密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('两次输入的新密码不一致！')
        return new_password2
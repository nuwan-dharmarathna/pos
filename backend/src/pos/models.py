from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.db.models.signals import pre_save
from django.dispatch import receiver


class User(AbstractUser):
    id = models.AutoField(primary_key=True)  # Custom primary key
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50, choices=[('cashier', 'Cashier'), ('manager', 'Manager')], default='cashier')
    is_active = models.BooleanField(default=True)
    # Add more fields as per your requirements
    class Meta:
        # Specify a unique related_name for the groups and user_permissions fields
        # to avoid clashes with the default 'auth.User' model
        default_related_name = 'pos_%(class)s'
    
class Product_Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.cat_name} : {self.date_updated}"


class Product_Unit(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Product_Category, on_delete=models.CASCADE, related_name="product_category"
    )

    def __str__(self):
        return f"{self.p_id} : {self.p_name}"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=64)
    unit_name = models.ForeignKey(
        Product_Unit, on_delete=models.CASCADE, related_name="product"
    )
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    stock_quantity = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} : {self.unit_name.p_name} : {self.stock_quantity} : {self.in_stock}"


class CustomPrimaryKeyField(models.AutoField):
    def pre_save(self, model_instance, add):
        if not model_instance.pk:
            today = date.today().strftime("%Y%m%d")
            last_sale = model_instance.__class__.objects.order_by('-pk').first()
            if last_sale:
                last_pk = last_sale.pk
                sequence_number = int(str(last_pk)[8:]) + 1
            else:
                sequence_number = 1

            model_instance.pk = int(f"{today}{sequence_number:03d}")

        return super().pre_save(model_instance, add)

class Sale(models.Model):
    id = CustomPrimaryKeyField(primary_key=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    cashier = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    customer_name = models.CharField(max_length=100)
    customer_phone_number = models.CharField(max_length=15, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('mobile_payment', 'Mobile Payment'),
        ('other', 'Other')
    ], default='cash')
    is_completed = models.BooleanField(default=False)
    _request = None

    def __str__(self):
        return f'{self.id} : {self.issue_date} : {self.cashier} : {self.is_completed}'


@receiver(pre_save, sender=Sale)
def set_cashier_on_save(sender, instance, **kwargs):
    if not instance.cashier_id:
        instance.cashier = instance._request.cashier

class SaleItem(models.Model):
    id = models.AutoField(primary_key=True)  # Implicit primary key
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


@receiver(pre_save, sender=SaleItem)
def update_unit_price_and_subtotal(sender, instance, **kwargs):
    # Calculate the unit_price based on the selected product
    instance.unit_price_at_sale = instance.product.price

    # Calculate the subtotal based on the quantity and unit_price
    instance.subtotal = instance.quantity * instance.unit_price_at_sale


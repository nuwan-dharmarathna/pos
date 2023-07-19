from django.db import models
from django.utils import timezone


# Create your models here.
class Product_Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=64)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cat_name} : {self.date_updated}"


class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=64)
    category = models.ForeignKey(
        Product_Category, on_delete=models.CASCADE, related_name="product_category"
    )

    def __str__(self):
        return f"{self.p_id} : {self.p_name}"


class Product_Unit(models.Model):
    unit_code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    product_name = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product"
    )
    expire_date = models.DateTimeField()
    purchase_price = models.FloatField()
    retail_price = models.FloatField()
    wholesale_price = models.FloatField()
    qty = models.IntegerField()
    in_stock = models.BooleanField()
    discount = models.FloatField()

    def __str__(self):
        return f"{self.name} : {self.product_name} : {self.qty} : {self.in_stock}"


class Bill(models.Model):
    bill_id = models.AutoField()
    issue_date = models.DateTimeField(default=timezone.now)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)

    def __str__(self):
        return f"{self.bill_id} : {self.issue_date} : "


class Bill_Items(models.Model):
    bill_code = models.ForeignKey(Bill, on_delete=models.CASCADE)
    unit_id = models.ForeignKey(Product_Unit, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)

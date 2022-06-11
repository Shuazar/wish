from django.db import models

# Create your models here.
from jsonfield import JSONField
from sqlalchemy import null


class TimeBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(TimeBaseModel):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name="ID User Telegram")
    username = models.CharField(max_length=100, verbose_name="Username Telegram", null=True)
    fullname = models.CharField(max_length=100, verbose_name="Full name", null=True)

    def __str__(self):
        return f"N'{self.id} ({self.user_id} - {self.username})"


class Referral(TimeBaseModel):
    class Meta:
        verbose_name = "Referral"
        verbose_name_plural = "Referrals"

    id = models.ForeignKey(User, unique=True, primary_key=True, on_delete=models.CASCADE)
    referrer_id = models.BigIntegerField()

    def __str__(self):
        return f"N'{self.id} - from {self.referrer_id}"


class Item(TimeBaseModel):
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Product Name", max_length=255)
    photo = models.CharField(verbose_name="Product Photo id", max_length=200)
    price = models.DecimalField(verbose_name="Price", decimal_places=2, max_digits=8)
    description = models.TextField(verbose_name="Description", max_length=3000, null=True)

    category_code = models.CharField(verbose_name="Category Code", max_length=20)
    category_name = models.CharField(verbose_name="Category Name", max_length=20)
    subcategory_code = models.CharField(verbose_name="Subcategory Code", max_length=20)
    subcategory_name = models.CharField(verbose_name="Subcategory Name", max_length=20)

    def __str__(self):
        return f"N'{self.id} - {self.name}"


class Purchase(TimeBaseModel):
    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"

    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, verbose_name="Buyer", on_delete=models.SET(0))
    item_id = models.ForeignKey(Item, verbose_name="Item ID", on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name="Amount", decimal_places=2, max_digits=8)
    quantity = models.IntegerField(verbose_name="Quantity")
    purchase_time = models.DateTimeField(verbose_name="Purchase Time", auto_now_add=True)
    shipping_address = JSONField(verbose_name="Shipping Address", null=True)
    phone_number = models.CharField(verbose_name="Phone Number", max_length=50)
    email = models.CharField(verbose_name="Email", max_length=100, null=True)
    receiver = models.CharField(verbose_name="Receiver name", max_length=100, null=True)
    successful = models.BooleanField(verbose_name="Successfully payment", default=False)

    def __str__(self):
        return f"N'{self.id} - {self.item_id} ({self.quantity})"

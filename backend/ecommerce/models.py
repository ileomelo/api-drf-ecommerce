from django.contrib.auth.models import User
from django.db import models
from django.utils.formats import localize
from django_extensions.db.models import (
    ActivatorModel,
    TimeStampedModel,
    TitleSlugDescriptionModel,
)
from utils.model_abstracts import Model

# Create your models here.


class Item(TimeStampedModel, ActivatorModel, TitleSlugDescriptionModel, Model):
    """
    ecommerce.Item
    Store a single item entry our shop
    """

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ["id"]

    def __str__(self) -> str:
        return self.title

    # Aqui começa o model pra valer
    stock = models.IntegerField(default=1)
    price = models.IntegerField(default=0)

    def amount(self):
        amount = localize(self.price)
        return amount

    def manage_stock(self, qty):  # qty = quantidade
        new_stock = self.stock - int(qty)
        self.stock = new_stock
        self.save()

    def check_stock(self, qty):
        # check if order quantity exceeds stock levels
        if int(qty) > self.stock:
            return False
        return True

    def place_order(self, user, qty):
        # used to place an order
        if self.check_stock(qty):
            order = Order.objects.create(item=self, quantity=qty, user=user)
            self.manage_stock(qty)
            return order
        else:
            return None


class Order(TimeStampedModel, ActivatorModel, Model):
    """
    ecommerce.Order
    Store a single order entry, related to model: "ecommerce.Item" and model:"auth.User"
    """

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["id"]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.item.title}"

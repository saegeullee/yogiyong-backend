from django.db         import models
from user.models       import User
from restaurant.models import *

class Order(models.Model):
    user              = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user_phone_number = models.CharField(max_length=15)
    order_request     = models.CharField(max_length=200)
    restaurant        = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    delivery_fee      = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_address  = models.CharField(max_length = 400)
    payment_method    = models.ForeignKey(PaymentMethods, on_delete=models.CASCADE)
    created_at        = models.DateTimeField(editable=False)
    menus             = models.ManyToManyField(Menus, through='JoinOrderMenu')

    class Meta:
        db_table = 'orders'

class JoinOrderMenu(models.Model):
    order  = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu   = models.ForeignKey(Menus, on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        db_table = 'join_order_menu'

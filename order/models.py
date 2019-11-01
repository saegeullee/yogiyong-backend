from django.db import models
from user.models import User

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table='orders'

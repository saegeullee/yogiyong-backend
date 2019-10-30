from django.db import models

class Orders(models.Model):
    user=models.ForeignKey(
        'user.Users',
        on_delete=models.CASCADE,
    )

	

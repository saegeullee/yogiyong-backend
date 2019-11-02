from django.db         import models
from user.models       import User
from restaurant.models import Restaurants, Menus
from order.models      import Order

class Review(models.Model):
    order           = models.ForeignKey(Order, on_delete=models.CASCADE)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant      = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    comment         = models.CharField(max_length=300)
    rating_taste    = models.DecimalField(max_digits=2, decimal_places=1)
    rating_delivery = models.DecimalField(max_digits=2, decimal_places=1)
    rating_quantity = models.DecimalField(max_digits=2, decimal_places=1)
    rating_avg      = models.DecimalField(max_digits=2, decimal_places=1)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    menus           = models.ManyToManyField(Menus, through='JoinReviewMenu')
    class Meta:
        db_table = 'reviews'

class ReviewImage(models.Model):
    review       = models.ForeignKey(Review, on_delete=models.CASCADE)
    review_imgae = models.CharField(max_length=4000)
    class Meta:
        db_table = 'review_images'

class JoinReviewMenu(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    menu   = models.ForeignKey(Menus, on_delete=models.CASCADE)
    amount = models.IntegerField()
    class Meta:
        db_table = 'join_review_menu'

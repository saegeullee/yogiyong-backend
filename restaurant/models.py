from django.db import models


class Restaurants(models.Model): 
    name                        = models.CharField(max_length=200)
    address                     = models.CharField(max_length=200)
    phone                       = models.CharField(max_length=100)
    lat                         = models.DecimalField(max_digits=15, decimal_places=12)
    lng                         = models.DecimalField(max_digits=15, decimal_places=12)
    phone_order                 = models.BooleanField(default=False)
    free_delivery_threshold     = models.DecimalField(max_digits=7, decimal_places=2)
    delivery_fee_explanation    = models.CharField(max_length=200)
    threshold                   = models.DecimalField(max_digits=7, decimal_places=2)
    logo_url                    = models.CharField(max_length=4000)
    estimated_delivery_time     = models.CharField(max_length=20)
    city                        = models.CharField(max_length=20)
    review_count                = models.IntegerField()
    open_time_description       = models.CharField(max_length=100, null=True)
    additional_discount         = models.IntegerField()
    review_image_count          = models.IntegerField()
    is_available_pickup         = models.BooleanField()
    delivery_fee                = models.DecimalField(max_digits=6, decimal_places=2)
    review_avg                  = models.IntegerField()
    one_dish                    = models.BooleanField()

    class Meta:
        db_table = "restaurants"

class Tags(models.Model):
    name            = models.CharField(max_length=100, blank=True)
    restaurant      = models.ManyToManyField(Restaurants, through='Restaurants_Tags')

    class Meta:
        db_table = "tags"

class Restaurants_Tags(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.SET_NULL, null=True)
    tag = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "restaurants_tags"

class PaymentMethods(models.Model):
    name            = models.CharField(max_length=100)
    restaurant      = models.ForeignKey(Restaurants, on_delete=models.CASCADE)

    class Meta:
        db_table = "payment_methods"

class Categories(models.Model):
    name             = models.CharField(max_length=50)
    restaurant       = models.ManyToManyField(Restaurants, through='Restaurants_Categories')

    class Meta:
        db_table = "categories"

class Restaurants_Categories(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "restaurants_categories"

class Menus(models.Model):
    restaurant          = models.ForeignKey(Restaurants, on_delete=models.SET_NULL, null=True)
    menu_category       = models.ForeignKey('MenuCategories', on_delete=models.SET_NULL, null=True)
    name                = models.CharField(max_length=100)
    description         = models.CharField(max_length=500)
    price               = models.DecimalField(max_digits=9, decimal_places=2)
    quantity            = models.IntegerField()
    image               = models.CharField(max_length=4000)

    class Meta:
        db_table="menus"

class MenuCategories(models.Model):
    restaurant          = models.ForeignKey(Restaurants, on_delete=models.SET_NULL, null=True)
    name                = models.CharField(max_length=100)

    class Meta:
        db_table="menucategories"

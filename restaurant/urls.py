from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.HomeView.as_view()),
    path('/category/<int:category_id>', views.CategoryView.as_view()), 
    path('/search', views.RestaurantsSearchView.as_view()), 
    path('/<int:restaurant_id>', views.RestaurantView.as_view()), 
]
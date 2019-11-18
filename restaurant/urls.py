from django.urls import path
from . import views

urlpatterns = [ 
    path('/categories', views.CategoriListView.as_view()),
    path('/category/<int:category_id>', views.CategoryView.as_view()), 
    path('/search', views.RestaurantsSearchView.as_view()), 
    path('/<int:restaurant_id>', views.RestaurantView.as_view()), 
]

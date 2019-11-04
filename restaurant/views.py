from django.http import JsonResponse
from django.views import View
from .models import Restaurants, Tags, PaymentMethods, Categories, Menus

import json


class HomeView(View):
    def get(self, request):
        
        return

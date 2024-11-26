from django.contrib import admin
from apps.svg.models import Transactions_coin
# Register your models here.
@admin.register(Transactions_coin)
class Transactions_coinAdmin(admin.ModelAdmin):
    list_display = ['from_user','to_user','amount','created_at']
    search_fields = ['created_at']
    
from django.contrib import admin
from .models import Menu, Item, Ingredient


class MenuAdmin(admin.ModelAdmin):
    search_fields = ['season']

admin.site.register(Menu, MenuAdmin)
admin.site.register(Item)
admin.site.register(Ingredient)
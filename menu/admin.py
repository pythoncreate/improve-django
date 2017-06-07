from django.contrib import admin
from .models import Menu, Item, Ingredient


class MenuAdmin(admin.ModelAdmin):
    search_fields = ['season']


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ('name',)

admin.site.register(Menu, MenuAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Ingredient)
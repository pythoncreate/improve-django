from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import *
from .forms import *


def menu_list(request):
    all_menus = Menu.objects.all().prefetch_related('items')
    menus = all_menus.filter(
        expiration_date__gte=timezone.now()
    ).order_by('expiration_date')
    return render(
        request,
        'menu/list_all_current_menus.html',
        {'menus': menus}
    )


def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try:
        item = Item.objects.select_related('chef').get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request, 'menu/item_detail.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()
            form.save_m2m()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/new_menu.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    items = Item.objects.all()
    admin = User.objects.get(username="admin")

    if request.method == "POST":
        ingredient = Ingredient(name="ingredient")
        ingredient.save()
        # put items in a list to save for later
        items = []

        # make new items from option box in template
        for i in request.POST.getlist('items'):
            item = Item(name=i, chef=admin, description = "your description here", standard=False)
            item.save()
            items.append(item)
            item.ingredients.add(ingredient)

        if not Menu.objects.filter(pk=pk).exists():
            menu=Menu(season=request.POST.get('season', ''),
                      expiration_date=datetime.strptime(request.POST.get('expiration_date', ''), '%m/%d/%Y'))

        else:
            menu=Menu.objects.get(pk=pk)
            # we will be replacing the old menu items
            menu.items.clear()

        menu.save()

        for item in items:
            menu.items.add(item)

        return redirect('menu_detail', pk=menu.pk)

    return render(request, 'menu/change_menu.html', {
    'menu': menu,
    'items': items,
})


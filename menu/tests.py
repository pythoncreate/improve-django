from django.core.urlresolvers import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from .models import Menu, Item, Ingredient
from .forms import MenuForm

menu1 = {
        "season": "Spring Menu",
        "expiration_date": "2017-06-21"
}

menu2 = {
        "season": "Fall Menu",
        "expiration_date": "2017-11-21"
}

items = []

class MenuViewsTests(TestCase):
    def setUp(self):
        self.chris = User.objects.create(username='chris', password='chris', email='chris@chris.com')
        ingredient1 = Ingredient(name='strawberry')
        ingredient1.save()
        ingredient2 = Ingredient(name='club soda')
        ingredient2.save()
        self.item1 = Item(
            id=5,
            name="Strawberry soda",
            description="delicious",
            chef=self.chris,
        )
        self.item1.save()
        items.append(self.item1)
        self.item1.ingredients.add(ingredient1, ingredient2)
        self.menu_one=Menu.objects.create(**menu1)
        self.menu_two=Menu.objects.create(**menu2)
        for item in items:
            self.menu_one.items.add(item)
        for item in items:
            self.menu_two.items.add(item)

    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu_one, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu_detail',
                                       kwargs={'pk': self.menu_one.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu_one,resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_item_detail_view(self):
        resp = self.client.get(reverse('item_detail',
                                       kwargs={'pk': self.item1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_detail.html')
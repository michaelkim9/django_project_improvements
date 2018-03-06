from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Menu, Item, Ingredient
from .forms import MenuForm


# kwargs for setting up menu data

menu1 = {
    'season': 'Summer',
    'expiration_date': timezone.now() + timedelta(days=365)
}

menu2 = {
    'season': 'Winter',
    'expiration_date': timezone.now() + timedelta(days=700)
}


class MenuViewsTests(TestCase):
    def setUp(self):

        self.user_one = User.objects.create(
            username='user_one',
            email='userone@gmail.com',
            password='testing123',
        )

        ingredient1 = Ingredient(name='Coconut')
        ingredient1.save()

        ingredient2 = Ingredient(name='Chocolate')
        ingredient2.save()

        self.item1 = Item(
            name='Item 1 Coco Choco',
            description='Coco Choco Drink',
            chef=self.user_one
        )
        self.item1.save()
        self.item1.ingredients.add(ingredient1, ingredient2)

        self.menu1 = Menu.objects.create(**menu1)
        self.menu1.items.add(self.item1)

        self.menu2 = Menu.objects.create(**menu2)
        self.menu2.items.add(self.item1)

    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu1, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, self.menu1.season)

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu_detail', kwargs={'pk': self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu1, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_item_detail_view(self):
        resp = self.client.get(reverse('item_detail', kwargs={'pk': self.item1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.item1, resp.context['item'])
        self.assertTemplateUsed(resp, 'menu/detail_item.html')

    def test_create_new_menu_view(self):
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')

    def test_edit_menu_view(self):
        resp = self.client.post(reverse('menu_edit', kwargs={'pk': self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')

    def test_menu_form(self):
        form = MenuForm({
            'season': 'Summer',
            'items': (1,),
            'expiration_date': timezone.now() + timedelta(days=365)
        })

        self.assertTrue(form.is_valid())
        menu = form.save()
        self.assertEqual(menu.season, 'Summer')
        self.assertEqual(menu.expiration_date.year, 2019)

    def test_menu_form_date(self):
        form_data = {
            'season': 'Summer',
            'items': self.item1,
            'expiration_date': '12/12/2019'
        }
        form = MenuForm(data=form_data)
        self.assertFalse(form.is_valid())

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from .forms import *


def menu_list(request):
    # Added prefetch related of menu items (manytomany fk field)
    # removed if statement and added filters, removed python sorting and
    # replaced with django .order

    all_menus = Menu.objects.all().prefetch_related('items')
    menus = all_menus.filter(expiration_date__gte=timezone.now()
                             ).order_by('expiration_date')
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    # replaced try with get object or 404
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    # Replaced try and except 404, with get object or 404
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    # added form.save_m2m(), we need for manytomany saving when we
    # have commit=False

    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            form.save_m2m()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    # used MenuForm
    # changed render request template to menu_edit from duplicated change menu.html
    # render form fields instead of other items
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_detail', pk=menu.pk)
    return render(request, 'menu/menu_edit.html', {'form': form})

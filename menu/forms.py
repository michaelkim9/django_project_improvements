from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone

from .models import Menu, Item, Ingredient


class MenuForm(forms.ModelForm):
    """added expiration date required formats and select date widget"""
    date_range = 5
    this_year = timezone.now().year
    expiration_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
        widget=forms.SelectDateWidget(
            years=range(this_year, this_year+date_range)
            )
    )

    class Meta:
        model = Menu
        fields = [
            'season',
            'items',
            'expiration_date',
        ]


    def clean_expiration_date(self):
        """added clean method so expiration date is greater than created_at"""
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date <= timezone.now():
            raise forms.ValidationError("Menu Expiration date should be a future date")
        return expiration_date

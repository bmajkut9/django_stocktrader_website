from django import forms

class AddCashForm(forms.Form):
    add_cash = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2, label='Amount')
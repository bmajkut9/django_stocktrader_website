from django import forms

class AddCashForm(forms.Form):
    add_cash = forms.DecimalField(max_digits=10, decimal_places=2, label='Amount')
    
class BuyForm(forms.Form):
    stock_amount = forms.IntegerField(label='Stock Amount', min_value=1)

class SellForm(forms.Form):
    stock_amount = forms.IntegerField(label='Stock Amount', min_value=1)
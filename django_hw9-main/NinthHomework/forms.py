from django import forms
from .models import Buyer, Seller, Product, Sale

class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = '__all__'

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
from django import forms
from payment.models import BillingAddress


class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['fname', 'lname', 'country', 'city', 'zipcode']
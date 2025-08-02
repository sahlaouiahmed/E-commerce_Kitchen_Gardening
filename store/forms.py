from django import forms
from .models import Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class ShippingForm(forms.Form):
    first_name = forms.CharField(max_length=100, initial="")
    last_name = forms.CharField(max_length=100, initial="")
    email = forms.EmailField(initial="")
    address = forms.CharField(max_length=255, initial="")
    city = forms.CharField(max_length=100, initial="")
    state = forms.CharField(max_length=100, initial="")
    zip_code = forms.CharField(max_length=10, initial="")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'stock']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('price', css_class='form-group col-md-6 mb-0'),
                Column('stock', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('image', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('category', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Changes')
        )

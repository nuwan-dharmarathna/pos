from django import forms


class CategoryForm(forms.Form):
    cat_name = forms.CharField(max_length=30)

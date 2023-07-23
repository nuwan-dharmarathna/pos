from django.shortcuts import render, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Sale
from . import models
from . import forms


# Create your views here.
class CategoryPageView(TemplateView):
    template_name = "category.html"


class CategoryListView(ListView):
    template_name = "category-list.html"
    queryset = models.Product_Category.objects.all()
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    template_name = "category-detail.html"
    queryset = models.Product_Category.objects.all()
    context_object_name = "category"


class CategoryCreateView(CreateView):
    template_name = "create_ctegory.html"
    form_class = forms.CategoryForm

    def get_success_url(self):
        return reverse("")


class CategoryUpdateView(UpdateView):
    template_name = "update_ctegory.html"
    queryset = models.Product_Category.objects.all()
    form_class = forms.CategoryForm

    def get_success_url(self):
        return reverse("")


class CategoryDeleteView(DeleteView):
    template_name = "delete_ctegory.html"
    queryset = models.Product_Category.objects.all()

    def get_success_url(self):
        return reverse("")


def create_sale(request):
    if request.method == 'POST':
        # Process form data and create a new Sale object
        sale = Sale.objects.create()
        sale._request = request
        # Save the Sale object
        sale.save()
        return render(request, 'success.html')
    else:
        # Render the form to create a new sale
        return render(request, 'create_sale.html')

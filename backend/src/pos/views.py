from django.shortcuts import render
from .models import Sale


# Create your views here.
def index(request):
    pass

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

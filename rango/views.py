from django.shortcuts import render
from rango.models import Category, Page

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': page_list,
    }
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')

def add_category(request):
    """Add a new category to the database"""
    category_saved = False
    
    if request.method == 'POST':
        category_name = request.POST.get('name')
        if category_name:
            category = Category(name=category_name)
            category.save()
            category_saved = True
    
    context_dict = {'category_saved': category_saved}
    return render(request, 'rango/add_category.html', context_dict)

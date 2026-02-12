from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm

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
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:index')
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})

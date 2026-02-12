from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

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

def show_category(request, category_name_slug):
    context_dict = {}
    
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context_dict)

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

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category is None:
        return redirect('rango:index')
    
    form = PageForm()
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['url'] and form.cleaned_data['url'].startswith('http'):
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect('rango:show_category', category_name_slug=category_name_slug)
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

def track_url(request):
    next_url = None
    if request.method == 'GET':
        if 'category_id' in request.GET:
            category_id = request.GET['category_id']
            try:
                category = Category.objects.get(id=category_id)
                category.likes += 1  # ← FIXED: likes not views!
                category.save()
                next_url = category.get_absolute_url()
            except:
                next_url = '/rango/'
        else:
            next_url = '/rango/'
    
    response = redirect(next_url)
    return response

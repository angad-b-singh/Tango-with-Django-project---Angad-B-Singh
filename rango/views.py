from django.shortcuts import render
from rango.models import Category, Page


def index(request):
    # Top 5 categories, ordered by likes (descending)
    category_list = Category.objects.order_by('-likes')[:5]
    # Top 5 pages, ordered by views (descending)
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': page_list,
    }

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    return render(request, 'rango/about.html')

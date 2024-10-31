from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from core.models import Book, Category, EJournal, Resource


@login_required
def home(request):
    categories = Category.objects.all()
    featured_books = Book.objects.all()[:3]
    featured_ejournal = EJournal.objects.order_by('-id')[:3] # Assuming 'id' is auto-incrementing, use '-created_at' if you have a datetime field
    # recent_reports = Report.objects.order_by('-date_published')[:3]
    return render(request, 'user/home.html', {
        'categories': categories,
        'featured_books': featured_books, 
        'featured_ejournal': featured_ejournal,
        # 'recent_reports': recent_reports,
    })

@login_required
def resources(request):
    return render(request, 'resources.html') # Create this template

@login_required
def reports(request):
    return render(request, 'reports.html') # Create this template

@login_required
def notifications(request):
    return render(request, 'notifications.html')  # Create this template

@login_required
def profile(request):
    return render(request, 'profile.html')  # Create this template


@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books = category.book_resources.all()  # Get all books in this category
    e_journals = category.ejournal_resources.all() # Get all e-journals in this category
    return render(request, 'user/category_detail.html', {
        'category': category,
        'books': books,
        'e_journals': e_journals,
    })

@login_required
def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, 'resource_detail.html', {'resource': resource})
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from django.db.models import CharField, Value, F
from core.models import Book, Category, EJournal, Report, Resource


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
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books = category.books.all()  # Get all books in this category
    e_journals = category.e_journals.all() # Get all e-journals in this category
    return render(request, 'user/category_detail.html', {
        'category': category,
        'books': books,
        'e_journals': e_journals,
    })

@login_required
def resources(request):
    books = Book.objects.all() 
    e_journals = EJournal.objects.all() 
    combined_resources = list(books) + list(e_journals) 
    combined_resources.sort(key=lambda x: x.date_published, reverse=True)
    for book in books:
        print(book.image.url)

    return render(request, 'user/resources.html', {'combined_resources': combined_resources})

@login_required
def resource_detail(request, resource_type,  pk):
    if resource_type == 'book':
        resource = get_object_or_404(Book, pk=pk)
    elif resource_type == 'e_journal':
        resource = get_object_or_404(EJournal, pk=pk)
    else:
        return redirect('core:home') # Handle invalid resource_type
    # Determine the specific resource type
    if isinstance(resource, Book):
        additional_fields = {
            'author': resource.author,
            'publisher': resource.publisher,
            'isbn': resource.isbn,
            'availability': resource.availability,
        }
    elif isinstance(resource, EJournal):
        additional_fields = {
            'publisher': resource.publisher,
            'issn': resource.issn,
        }
    else:
        resource_type = 'unknown'
        additional_fields = {}

    return render(request, 'user/resource_detail.html', {
        'resource': resource,
        'resource_type': resource_type,
        **additional_fields
    })

@login_required
def reports(request):
    all_reports = Report.objects.order_by('-date_published') # Sort by date_published descending
    return render(request, 'user/reports.html', {'all_reports': all_reports})

@login_required
def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'user/report_detail.html', {'report': report})

@login_required
def notifications(request):
    return render(request, 'notifications.html')  # Create this template

@login_required
def profile(request):
    return render(request, 'profile.html')  # Create this template


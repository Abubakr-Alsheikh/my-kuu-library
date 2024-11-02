from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.utils import timezone
from django.db.models import Q
from core.decorators import admin_required
from core.models import Book, Category, EJournal, Notification, Report, ViewedResource
from django.contrib import messages

class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True  # Redirect authenticated users

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')  # Get the remember_me value
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if remember_me:
                # Set a longer session expiry (1 hour)
                self.request.session.set_expiry(timedelta(hours=1).seconds)
            else:
                # Set a shorter session expiry (or default, which is browser session)
                self.request.session.set_expiry(0) # Session expires when browser closes.
            if user.is_staff:
                login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('core:dashboard') # Redirect to admin if is_staff
            else:
                login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('core:home')  #Redirect to home page otherwise.
        else:
            return self.form_invalid(form) #Handle invalid login

@login_required
def home(request):
    categories = Category.objects.all()

    # Combine Book and EJournal queries
    featured_resources = list(Book.objects.all()[:3]) + list(EJournal.objects.all()[:3])
    featured_resources.sort(key=lambda x: x.date_published, reverse=True) #Sort by date published

    return render(request, 'home/home.html', {
        'categories': categories,
        'featured_resources': featured_resources,
    })


@login_required
def search(request):
    query = request.GET.get('q')

    if query:
        # Search in books, e-journals (using only title and description)
        books_results = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        ).all()
        e_journals_results = EJournal.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).all()

        # Combine the results into a single list of dictionaries
        results = list(books_results) + list(e_journals_results)

        return render(request, 'home/search_results.html', {'results': results, 'query': query}) # Pass query for display
    else:
        return render(request, 'home/search_results.html', {'query': query}) # No query

@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # Combine Book and EJournal queries for the category
    resources = list(category.books.all()) + list(category.e_journals.all())
    resources.sort(key=lambda x: x.date_published, reverse=True)

    return render(request, 'home/category_detail.html', {
        'category': category,
        'resources': resources,
    })

@login_required
def resources(request):
    books = Book.objects.all() 
    e_journals = EJournal.objects.all() 
    combined_resources = list(books) + list(e_journals) 
    combined_resources.sort(key=lambda x: x.date_published, reverse=True)
    for book in books:
        print(book.image.url)

    return render(request, 'home/resources.html', {'combined_resources': combined_resources})

@login_required
def resource_detail(request, resource_type,  pk):
    if resource_type == 'book':
        resource = get_object_or_404(Book, pk=pk)
    elif resource_type == 'e_journal':
        resource = get_object_or_404(EJournal, pk=pk)
    else:
        return redirect('core:home') # Handle invalid resource_type

    # Check if a ViewedResource entry already exists
    try:
        viewed_resource = ViewedResource.objects.get(
            user=request.user,
            resource_type=resource_type,
            resource_id=resource.id
        )
        # Update the date_viewed and increment view count
        viewed_resource.date_viewed = timezone.now()
        viewed_resource.view_count += 1
        viewed_resource.save()
    except ViewedResource.DoesNotExist:
        # Create a new ViewedResource entry
        viewed_resource = ViewedResource(
            user=request.user,
            resource_type=resource_type,
            resource_id=resource.id,
            date_viewed=timezone.now()
        )
        viewed_resource.save()

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

    return render(request, 'home/resource_detail.html', {
        'resource': resource,
        'resource_type': resource_type,
        **additional_fields
    })

@login_required
def reports(request):
    all_reports = Report.objects.order_by('-date_published') # Sort by date_published descending
    return render(request, 'home/reports.html', {'all_reports': all_reports})

@login_required
def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'home/report_detail.html', {'report': report})

# --------------- User Profile Logic

@login_required
def profile(request):
    viewed_resources = ViewedResource.objects.filter(user=request.user).order_by('-date_viewed')
    
    # Fetch resources from the database based on viewed_resources
    resources = []
    for viewed_resource in viewed_resources:
        if viewed_resource.resource_type == 'book':
            resource = Book.objects.get(pk=viewed_resource.resource_id)
        elif viewed_resource.resource_type == 'e_journal':
            resource = EJournal.objects.get(pk=viewed_resource.resource_id)
        resources.append({
            'resource': resource,
            'resource_type': viewed_resource.resource_type,
            'date_viewed': viewed_resource.date_viewed,
            'get_resource_url': viewed_resource.get_resource_url()
        })

    return render(request, 'user/profile.html', {'resources': resources})


@login_required
def user_reports(request):
    all_reports = Report.objects.filter(author=request.user).order_by('-date_published')
    return render(request, 'user/reports.html', {'all_reports': all_reports})

@login_required
def add_report(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            new_report = Report(title=title, content=content, author=request.user)
            new_report.save()
            messages.success(request, 'Report created successfully!')
            return redirect('core:user_reports')
        else:
            messages.error(request, 'Please fill in all fields.')
    return render(request, 'user/add_report.html')

@login_required
def notifications(request):
    notifications = Notification.objects.all().order_by('-timestamp') #Get all notifications, newest first
    context = {
        'notifications': notifications
    }
    return render(request, 'user/notifications.html', context)

# --------------- Dashboard Logic

@admin_required
def dashboard_home(request):
    return render(request, 'dashboard/home.html')

@admin_required
def user_management(request):
    return render(request, 'dashboard/user_management.html')

@admin_required
def resource_management(request):
    return render(request, 'dashboard/resource_management.html')

@admin_required
def category_management(request):
    return render(request, 'dashboard/category_management.html')

@admin_required
def notification_management(request):
        return render(request, 'dashboard/notification_management.html')


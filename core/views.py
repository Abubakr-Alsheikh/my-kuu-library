from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.utils import timezone
from django.db.models import Q
from core.decorators import admin_required
from core.forms import BookForm, CategoryForm, EJournalForm, NotificationForm, UserForm
from core.models import AuditLog, Book, Category, EJournal, Notification, Report, ViewedResource
from django.contrib import messages
from django.contrib.auth.models import User

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
    latest_actions = AuditLog.objects.all().order_by('-timestamp')
    return render(request, 'dashboard/home.html', {'latest_actions': latest_actions})

@admin_required
def user_management(request):
    if request.user.is_staff:
        users = User.objects.filter(is_superuser=False).order_by('username')
        return render(request, 'dashboard/user_management.html', {'users': users})
    else:
        return redirect('core:home')

@admin_required
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            AuditLog.objects.create(
                action="User created", user=request.user, type="user", type_id=new_user.id
            )
            messages.success(request, 'User created successfully!')
            return redirect('core:user_management')
        else:
            errMsg = [(k, v[0]) for k, v in form.errors.items()]
            messages.error(request, f'Invalid form submission. {errMsg[0][1]}')
    else:
        form = UserForm()
    return render(request, 'dashboard/user_form.html', {'form': form})

@admin_required
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            AuditLog.objects.create(
                action="User updated", user=request.user, type="user", type_id=user.id
            )
            messages.success(request, 'User updated successfully!')
            return redirect('core:user_management')
        else:
            errMsg = [(k, v[0]) for k, v in form.errors.items()]
            messages.error(request, f'Invalid form submission. {errMsg[0][1]}')
    else:
        form = UserForm(instance=user)
    return render(request, 'dashboard/user_form.html', {'form': form})

@admin_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_id = user.id # Store user ID before deletion
    user.delete()
    AuditLog.objects.create(
        action="User deleted", user=request.user, type="user", type_id=user_id
    )
    messages.success(request, 'User deleted successfully!')
    return redirect('core:user_management')


@admin_required
def resource_management(request):
    if request.user.is_staff:
        # Combine Book and EJournal queries
        resources = list(Book.objects.all()) + list(EJournal.objects.all())
        resources.sort(key=lambda x: x.date_published, reverse=True)

        return render(request, 'dashboard/resource_management.html', {'resources': resources})
    else:
        return redirect('core:home')

@admin_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)  # Create the Book object but don't save yet
            book.resource_type = 'book'  # Set the resource_type
            book.published_by = request.user  # Set the published_by (admin user)
            book.availability = True  # Set availability to True (default)
            book.save()
            AuditLog.objects.create(
                action="Book created", user=request.user, type="book", type_id=book.id
            )
            messages.success(request, 'Book created successfully!')
            return redirect('core:resource_management')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = BookForm()
        categories = Category.objects.all()
    return render(request, 'dashboard/resource_form.html', {'form': form, 'resource_type': 'book', 'categories': categories})

@admin_required
def add_e_journal(request):
    if request.method == 'POST':
        form = EJournalForm(request.POST, request.FILES)
        if form.is_valid():
            e_journal = form.save(commit=False) 
            e_journal.resource_type = 'e_journal'  # Set the resource_type
            e_journal.published_by = request.user # Set the published_by (admin user)
            e_journal.availability = True # Set availability to True (default)
            e_journal.save()
            AuditLog.objects.create(
                action="E-Journal created", user=request.user, type="e_journal", type_id=e_journal.id
            )
            messages.success(request, 'E-Journal created successfully!')
            return redirect('core:resource_management')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = EJournalForm()
        categories = Category.objects.all()
    return render(request, 'dashboard/resource_form.html', {'form': form, 'resource_type': 'e_journal', 'categories': categories})


@admin_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            AuditLog.objects.create(
                action="Book updated", user=request.user, type="book", type_id=book.id
            )
            messages.success(request, 'Book updated successfully!')
            return redirect('core:resource_management')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = BookForm(instance=book)
        categories = Category.objects.all()
    return render(request, 'dashboard/resource_form.html', {'form': form, 'resource_type': 'book', 'categories': categories})

@admin_required
def edit_e_journal(request, pk):
    e_journal = get_object_or_404(EJournal, pk=pk)
    if request.method == 'POST':
        form = EJournalForm(request.POST, request.FILES, instance=e_journal)
        if form.is_valid():
            form.save()
            AuditLog.objects.create(
                action="E-Journal updated", user=request.user, type="e_journal", type_id=e_journal.id
            )
            messages.success(request, 'E-Journal updated successfully!')
            return redirect('core:resource_management')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = EJournalForm(instance=e_journal)
        categories = Category.objects.all()
    return render(request, 'dashboard/resource_form.html', {'form': form, 'resource_type': 'e_journal', 'categories': categories})

@admin_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book_id = book.id
    book.delete()
    AuditLog.objects.create(
        action="Book deleted", user=request.user, type="book", type_id=book_id
    )
    messages.success(request, 'Book deleted successfully!')
    return redirect('core:resource_management')

@admin_required
def delete_e_journal(request, pk):
    e_journal = get_object_or_404(EJournal, pk=pk)
    e_journal_id = e_journal.id
    e_journal.delete()
    AuditLog.objects.create(
        action="E-Journal deleted", user=request.user, resource_type="e_journal", resource_id=e_journal_id
    )
    messages.success(request, 'E-Journal deleted successfully!')
    return redirect('core:resource_management')

@admin_required
def category_management(request):
    if request.user.is_staff:
        categories = Category.objects.all()
        return render(request, 'dashboard/category_management.html', {'categories': categories})
    else:
        return redirect('core:home')

@admin_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()  # Save the category
            AuditLog.objects.create(
                action="Category created",
                user=request.user,
                type="category",
                type_id=category.id,
            )
            messages.success(request, 'Category created successfully!')
            return redirect('core:category_management')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form})

@admin_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            AuditLog.objects.create(
                action="Category updated",
                user=request.user,
                type="category",
                type_id=category.id,
            )
            messages.success(request, 'Category updated successfully!')
            return redirect('core:category_management')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form})

@admin_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category_id = category.id  # Store category ID before deletion
    category.delete()
    AuditLog.objects.create(
        action="Category deleted",
        user=request.user,
        type="category",
        type_id=category_id,
    )
    messages.success(request, 'Category deleted successfully!')
    return redirect('core:category_management')

@admin_required
def notification_management(request):
    if request.user.is_staff:
        notifications = Notification.objects.all().order_by('-timestamp')
        return render(request, 'dashboard/notification_management.html', {'notifications': notifications})
    else:
        return redirect('core:home')

@admin_required
def add_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.sender = request.user  # Set sender to the current admin
            notification.save() 
            AuditLog.objects.create(
                action="Notification created",
                user=request.user,
                type="notification",
                type_id=notification.id,
            )
            messages.success(request, 'Notification created successfully!')
            return redirect('core:notification_management')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = NotificationForm()
        users = User.objects.all()
        return render(request, 'dashboard/notification_form.html', {'form': form, 'users': users})

@admin_required
def edit_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=notification)
        if form.is_valid():
            form.save()
            AuditLog.objects.create(
                action="Notification updated",
                user=request.user,
                type="notification",
                type_id=notification.id,
            )
            messages.success(request, 'Notification updated successfully!')
            return redirect('core:notification_management')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = NotificationForm(instance=notification)
        users = User.objects.all()
        return render(request, 'dashboard/notification_form.html', {'form': form, 'users': users})

@admin_required
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification_id = notification.id
    notification.delete()
    AuditLog.objects.create(
        action="Notification deleted",
        user=request.user,
        type="notification",
        type_id=notification_id,
    )
    messages.success(request, 'Notification deleted successfully!')
    return redirect('core:notification_management')
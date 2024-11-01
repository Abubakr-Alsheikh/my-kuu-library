from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(
        max_length=100, unique=True
    )  # Ensure category names are unique
    description = models.TextField(
        blank=True, null=True
    )  # Optional description for the category
    image = models.ImageField(
        upload_to="category_images/", blank=True, null=True
    )  # Upload category images (optional)

    def get_absolute_url(self):
        return reverse("core:category_detail", args=[str(self.id)])


class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="resource_images/", blank=True, null=True)
    published_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_published",
    )  # Generic related_name
    date_published = models.DateTimeField(auto_now_add=True)
    availability = models.BooleanField(default=True)
    resource_type = models.CharField(max_length=20, choices=[('book', 'Book'), ('e_journal', 'E-Journal')], null=True, blank=True)

    class Meta:
        abstract = True
        
    
    def get_absolute_url(self):
        return reverse('core:resource_detail', args=[self.resource_type, str(self.id)])


class Book(Resource):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="books"
    )
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, blank=True, null=True)


class EJournal(Resource):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="e_journals"
    )
    publisher = models.CharField(max_length=255)
    issn = models.CharField(max_length=20, blank=True, null=True)


class Report(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()  # Use TextField for larger content
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='published_reports')
    date_published = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def get_absolute_url(self):
        return reverse('core:report_detail', args=[str(self.id)])
    

class ViewedResource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=20)  # e.g., 'book', 'e_journal'
    resource_id = models.IntegerField()
    date_viewed = models.DateTimeField(default=timezone.now)
    view_count = models.IntegerField(default=0)

    def get_resource_url(self):
        return reverse('core:resource_detail', args=[self.resource_type, self.resource_id])

    def __str__(self):  # For easier debugging in admin
        return f"{self.user.username} viewed {self.resource_type} {self.resource_id} on {self.date_viewed}"

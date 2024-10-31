from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse


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

    class Meta:
        abstract = True


class Book(Resource):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="books"
    )
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("core:resource_detail", args=[str("book"), str(self.id)])


class EJournal(Resource):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="e_journals"
    )
    publisher = models.CharField(max_length=255)
    issn = models.CharField(max_length=20, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("core:resource_detail", args=[str("e_journal"), str(self.id)])

from django.contrib import admin

from .models import Category, Book, EJournal, Report

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(EJournal)
admin.site.register(Report)
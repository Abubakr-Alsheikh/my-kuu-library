from django.contrib import admin

from .models import Category, Book, EJournal, Notification, Report, ViewedResource

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(EJournal)
admin.site.register(Report)
admin.site.register(ViewedResource)
admin.site.register(Notification)
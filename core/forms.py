from django import forms
from django.contrib.auth.models import User

from core.models import Book, Category, EJournal


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff']

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        
        # Only update the password if a new one has been provided
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
        
        return user


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'image', 'author', 'publisher', 'isbn', 'category']

class EJournalForm(forms.ModelForm):
    class Meta:
        model = EJournal
        fields = ['title', 'description', 'image', 'publisher', 'issn', 'category']
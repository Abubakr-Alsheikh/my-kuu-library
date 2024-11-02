from django import forms
from django.contrib.auth.models import User


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
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from apps.users.models import User
from apps.users.validators.superuser import valid_password


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, validators=[valid_password]
    )
    password_confirm = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        validators=[valid_password],
    )

    class Meta:
        model = User
        fields = ("name", "email", "password")

    def clean_password_confirmation(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords don't match")
        return password_confirmation

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("name", "email", "password")

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "id",
        "name",
        "email",
        "is_admin",
    )
    list_display_links = ("id", "name")
    list_filter = ("is_admin",)
    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "name",
                    "email",
                    "password",
                )
            },
        ),
        ("Status", {"fields": ("is_admin", "is_active")}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "email",
                    "password",
                    "password_confirmation",
                ),
            },
        ),
    )
    search_fields = ("email", "name", "document")
    ordering = ("name",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    list_per_page = 15

admin.site.register(User, UserAdmin)

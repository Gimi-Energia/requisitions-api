from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django import forms
from apps.users.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "phone",
            "type",
            "company",
            "department",
            "is_active",
            "is_admin",
            "groups",
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "phone",
            "type",
            "company",
            "department",
            "password",
            "is_active",
            "is_admin",
            "groups",
        )

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "id",
        "name",
        "email",
        "company",
        "department",
        "type",
        "is_admin",
        "is_active",
        "date_joined",
    )
    list_display_links = ("id", "email")
    search_fields = ("name", "email")
    list_filter = ("is_admin", "type", "is_active", "company", "department")
    list_per_page = 25
    ordering = ("name", "email")

    readonly_fields = ("date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name", "phone", "type")}),
        (_("Company info"), {"fields": ("company", "department")}),
        (_("Permissions"), {"fields": ("is_admin", "is_active", "groups")}),
        (_("Important dates"), {"fields": ("date_joined",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "email",
                    "phone",
                    "password1",
                    "password2",
                    "type",
                    "company",
                    "department",
                    "is_active",
                    "is_admin",
                    "groups",
                ),
            },
        ),
    )

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj)


admin.site.register(User, UserAdmin)

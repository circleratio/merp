from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group 
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
#                    "groups",
#                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    list_display = ("username", "email", "is_staff")
#    list_filter = ("is_staff", "is_superuser", "groups")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("username", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

CustomUser = get_user_model()
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)  # Groupモデルは不要のため非表示


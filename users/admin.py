from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
)

from .models import (
    BaseUserModel,
    Staff,
    Admin,
    Client,
    Vendor,
)

def all_field_names(model):
    return tuple(f.name for f in model._meta.fields)



@admin.register(BaseUserModel)
class UserAdmin(PolymorphicParentModelAdmin, BaseUserAdmin):
    base_model = BaseUserModel
    child_models = (Admin, Staff, Client, Vendor)

    list_display = all_field_names(BaseUserModel)
    search_fields = ("email",)
    ordering = ("-updated_at",)
    list_filter = ("is_active", "is_staff", "is_superuser", "updated_at")



@admin.register(Staff)
class StaffAdmin(PolymorphicChildModelAdmin):
    base_model = Staff

    list_display = all_field_names(BaseUserModel)
    search_fields = ("email", "full_name")
    ordering = ("-updated_at",)
    list_filter = ("is_active",)
    fields = all_field_names(BaseUserModel)


@admin.register(Admin)
class AdminAdmin(PolymorphicChildModelAdmin):
    base_model = Admin

    list_display = all_field_names(BaseUserModel)
    search_fields = ("email", "full_name")
    ordering = ("-updated_at",)
    list_filter = ("is_active",)
    fields = all_field_names(BaseUserModel)


@admin.register(Vendor)
class VendorAdmin(PolymorphicChildModelAdmin):
    base_model = Vendor

    list_display = all_field_names(BaseUserModel)
    search_fields = ("email", "full_name")
    ordering = ("-updated_at",)
    list_filter = ("is_active",)
    fields = all_field_names(BaseUserModel)


@admin.register(Client)
class ClientAdmin(PolymorphicChildModelAdmin):
    base_model = Client

    list_display = all_field_names(BaseUserModel)
    search_fields = ("email", "full_name")
    ordering = ("-updated_at",)
    list_filter = ("is_active",)
    fields = all_field_names(BaseUserModel)

from django.contrib import admin
from .models import Category, Maqale, Comment, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)


@admin.register(Maqale)
class MaqaleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "created_at", "updated_at")
    search_fields = ("title", "matn", "author__username", "category__title")
    list_filter = ("created_at", "updated_at", "category")
    prepopulated_fields = {"slug": ("title",)}

    def _is_author(self, request):
        return request.user.is_superuser or request.user.groups.filter(name="authors").exists()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return self._is_author(request)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return self._is_author(request)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return self._is_author(request)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return self._is_author(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return self._is_author(request)

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "maqale", "parent", "is_active", "is_edited", "created_at")
    search_fields = ("author__username", "maqale__title", "text")
    list_filter = ("is_active", "is_edited", "created_at")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "maqale")
    search_fields = ("user__username", "maqale__title")

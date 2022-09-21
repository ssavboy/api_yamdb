from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug"')
    search_fields = ('name',)


class GenreAdmin(CategoryAdmin):
    pass


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'year', 'description')
    search_fields = ('name', 'year')
    list_filter = ('category',)


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)

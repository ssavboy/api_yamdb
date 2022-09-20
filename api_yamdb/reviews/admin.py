from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date',)
    search_fields = ('review', 'text', 'author', 'pub_date',)
    list_filter = ('review', 'text', 'author', 'pub_date',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'score', 'author', 'pub_date',)
    search_fields = ('title', 'text', 'author', 'pub_date',)
    list_filter = ('title', 'text', 'score', 'author', 'pub_date',)

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)


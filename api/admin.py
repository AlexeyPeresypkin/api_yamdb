from django.contrib import admin

# Register your models here.
from api.models import Review, Title, Genre, Comments, Category


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category',)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Comments)
admin.site.register(Category)

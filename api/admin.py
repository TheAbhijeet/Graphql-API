from django.contrib import admin
from .models import Post, Page, Comment, User, Category, Tag, user_actions
# Register your models here.

admin.site.register(Post)
admin.site.register(Page)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(user_actions)
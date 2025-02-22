from django.contrib import admin
from api import models as api_models


# Admin Models
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']
    list_editable = ['image']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(api_models.User)
admin.site.register(api_models.Profile)
admin.site.register(api_models.Category, CategoryAdmin)
admin.site.register(api_models.Post)
admin.site.register(api_models.Comment)
admin.site.register(api_models.Bookmark)
admin.site.register(api_models.Notification)
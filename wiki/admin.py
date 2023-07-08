from django.contrib import admin

from wiki.models import (
    Article,
    Section,
    ArticleComment,
    Moderation,
    History,
    Role,
    UserProfile,
)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "created_by", "created_at")


class SectionAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "parent")


admin.site.register(Section, SectionAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment)
admin.site.register(Moderation)
admin.site.register(History)
admin.site.register(Role)
admin.site.register(UserProfile)

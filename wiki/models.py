from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

from accounts.models import CustomUser


class Photo(models.Model):
    image = models.ImageField(upload_to="photos/")


class Section(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = CKEditor5Field(verbose_name="Описание", config_name="extends")
    parent = models.ForeignKey("self", verbose_name="Родитель", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def get_ancestors(self):
        ancestors = []
        node = self.parent
        while node:
            ancestors.append(node)
            node = node.parent
        return ancestors

    def get_absolute_url(self):
        return reverse("section_detail", args=[str(self.id)])

    def __str__(self):
        return self.title


class Article(models.Model):
    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    content = CKEditor5Field(verbose_name="Контент", config_name="extends")
    sidebar_content = CKEditor5Field(verbose_name="Боковой блок", config_name="extends", blank=True, null=True)
    section = models.ForeignKey(
        Section, verbose_name="Раздел", on_delete=models.CASCADE, related_name="articles"
    )
    main_photo = models.ImageField(verbose_name="Главная фотография", upload_to="article_photos/", blank=True)
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус статьи', max_length=10)
    created_by = models.ForeignKey(
        CustomUser, verbose_name='Автор', on_delete=models.CASCADE, related_name="articles_created"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    updated_by = models.ForeignKey(
        CustomUser,
        verbose_name='Обновил',
        on_delete=models.CASCADE,
        related_name="updated_articles",
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at', 'status'])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def get_absolute_url(self):
        return reverse("article_detail", args=[str(self.id)])

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    content = CKEditor5Field(
        max_length=500, verbose_name="Comment", config_name="extends"
    )
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="article_comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_comments"
    )


class Moderation(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="moderations"
    )
    moderated_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="moderations"
    )
    moderated_at = models.DateTimeField(auto_now_add=True)


class History(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="histories"
    )
    changed_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="histories"
    )
    changed_at = models.DateTimeField(auto_now_add=True)
    content_before = models.TextField()
    content_after = models.TextField()


class Role(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="roles")


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    comments = models.ManyToManyField(ArticleComment, related_name="profiles")
    edits = models.IntegerField(default=0)

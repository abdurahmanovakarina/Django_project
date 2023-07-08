from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Section, Article
from .singleton import SectionTree


@receiver(post_save, sender=Article)
def article_created(sender, instance, created, **kwargs):
    if created:
        print(f"Article {instance.title} created")


@receiver(post_save, sender=Section)
@receiver(post_save, sender=Article)
def update_section_tree(sender, **kwargs):
    SectionTree().update_tree()

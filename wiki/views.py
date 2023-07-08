from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import DetailView

from accounts.models import CustomUser
from wiki.forms import ArticleCreateForm, ArticleUpdateForm
from wiki.models import Article, Section, Photo


def index(request):
    return render(request, "wiki/index.html")


@login_required
def create_article(request):
    if CustomUser.objects.get(pk=request.user.id).is_banned:
        return render(request, "registration/banned.html")
    if request.method == "POST":
        form = ArticleCreateForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.created_by = request.user
            article.updated_by = None
            article.save()
            form.save_m2m()  # Сохранение связанных объектов ManyToMany

            files = request.FILES.getlist('gallery_photos')
            if files:
                for file in files:
                    photo = Photo.objects.create(image=file)
                    article.gallery_photos.add(photo)
            article.save()

            return redirect("article_detail", article_id=article.pk)
    else:
        form = ArticleCreateForm()
    return render(request, "wiki/create_article.html", {"form": form})


@login_required
def update_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if CustomUser.objects.get(pk=request.user.id).is_banned:
        return render(request, "registration/banned.html")
    if request.method == "POST":
        form = ArticleUpdateForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.updated_by = request.user
            article.updated_at = timezone.now()
            if "main_photo" in request.FILES:
                article.main_photo = request.FILES["main_photo"]

            files = request.FILES.getlist('gallery_photos')
            if files:
                for file in files:
                    photo = Photo.objects.create(image=file)
                    article.gallery_photos.add(photo)
            article.save()
            messages.success(request, "Article updated successfully.")
            return redirect("article_detail", article_id=article.pk)
    else:
        form = ArticleUpdateForm(instance=article)
    return render(request, "wiki/update_article.html", {"form": form})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, "wiki/article_detail.html", {"article": article})


class SectionDetailView(DetailView):
    model = Section
    template_name = "wiki/section_detail.html"


def error_404_view(request, exception):
    return render(request, "errors/404.html")

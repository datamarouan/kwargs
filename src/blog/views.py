from .models import *
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, View, TemplateView

def index(request):
    article_tout = Article.objects.all()
    brouillons = article_tout.filter(published=False)
    publications = article_tout.filter(published=True)
    headline = article_tout.last()
    context = {
        'brouillons':brouillons,
        'publications':publications,
        "headline":headline
    }
    return render(request, 'blog/accueil.html', context)

class ArticleListView(ListView):
    model = Article
    template_name = "blog/crud/articles_list.html"

class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/crud/article_details.html"

class ArticleCreateView(CreateView, LoginRequiredMixin, SuccessMessageMixin):
    model = Article
    fields = '__all__'
    template_name = "blog/crud/article_ajout.html"

class ArticleUpdateView(UpdateView, LoginRequiredMixin, SuccessMessageMixin):
    model = Article
    fields = '__all__'
    template_name = "blog/crud/article_ajout.html"

class ArticleDeleteView(DeleteView, LoginRequiredMixin, SuccessMessageMixin):
    model = Article
    template_name = "objet_a_effacer.html"
    success_url = '/blog/articles/'
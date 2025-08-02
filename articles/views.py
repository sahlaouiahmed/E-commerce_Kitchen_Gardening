from django.shortcuts import render, get_object_or_404
from .models import Article

def article_list(request):
    query = request.GET.get('q', '')
    if query:
        articles = Article.objects.filter(title__icontains=query).order_by('-published_date')
    else:
        articles = Article.objects.all().order_by('-published_date')
    context = {
        'articles': articles,
        'query': query,
    }
    return render(request, 'articles/article_list.html', context)




def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/article_detail.html', {'article': article})


#SUPERUSER
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Article
from .forms import ArticleForm

def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

@superuser_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article added successfully!')
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'articles/add_article.html', {'form': form})

@superuser_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/edit_article.html', {'form': form, 'article': article})


@superuser_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted successfully!')
        return redirect('article_list')
    return render(request, 'articles/confirm_delete.html', {'article': article})

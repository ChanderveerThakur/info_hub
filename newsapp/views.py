from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SearchHistory
from .utils import fetch_news

@login_required
def home(request):
    lang = request.GET.get('lang', 'en')
    query = request.GET.get('q', '')
    user = request.user

    if query:
        articles = fetch_news(query, lang)
        if articles:
            SearchHistory.objects.create(
                user=user,
                query=query,
                title=articles[0].get('title', ''),
                url=articles[0].get('url', ''),
                language=lang
            )
        return render(request, 'newsapp/search_results.html', {'articles': articles, 'query': query, 'lang': lang})

    articles = fetch_news('latest', lang)
    history = SearchHistory.objects.filter(user=user)[:10]
    return render(request, 'newsapp/home.html', {'articles': articles, 'recent_history': history, 'lang': lang})

@login_required
def history_view(request):
    history = SearchHistory.objects.filter(user=request.user)
    return render(request, 'newsapp/history.html', {'history': history})

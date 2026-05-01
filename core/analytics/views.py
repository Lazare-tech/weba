from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from abonnements.decorators import require_plan
from .services import (
    get_stats_globales,
    get_pages_populaires,
    get_sources_trafic,
    get_pays,
    get_series_temporelle,
)


@login_required
@require_plan('pro', 'business')
def dashboard_analytics(request):
    profil = request.user.profil
    domaine = None
    stats = None
    pages = []
    sources = []
    pays = []
    series = []
    periode = request.GET.get('periode', '30d')

    try:
        site = request.user.site_plausible
        domaine = site.domaine
        stats = get_stats_globales(domaine, periode)
        pages = get_pages_populaires(domaine, periode)
        sources = get_sources_trafic(domaine, periode)
        pays = get_pays(domaine, periode)
        series = get_series_temporelle(domaine, periode)
    except Exception:
        pass

    return render(request, 'analytics/dashboard.html', {
        'profil': profil,
        'domaine': domaine,
        'stats': stats,
        'pages': pages,
        'sources': sources,
        'pays': pays,
        'series': series,
        'periode': periode,
    })


@login_required
def stats_rapides(request):
    try:
        site = request.user.site_plausible
        stats = get_stats_globales(site.domaine, '7d')
    except Exception:
        stats = None

    return render(request, 'analytics/partials/stats_rapides.html', {
        'stats': stats
    })
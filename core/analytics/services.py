import requests
from django.conf import settings

PLAUSIBLE_URL = getattr(settings, 'PLAUSIBLE_URL', 'http://localhost:8001')
PLAUSIBLE_API_KEY = getattr(settings, 'PLAUSIBLE_API_KEY', '')


def get_headers():
    return {
        'Authorization': f'Bearer {PLAUSIBLE_API_KEY}',
        'Content-Type': 'application/json',
    }


def creer_site_plausible(domaine):
    try:
        response = requests.post(
            f'{PLAUSIBLE_URL}/api/v1/sites',
            headers=get_headers(),
            json={'domain': domaine, 'timezone': 'Africa/Ouagadougou'},
            timeout=5
        )
        return response.status_code == 200
    except Exception:
        return False


def get_stats_globales(domaine, periode='30d'):
    try:
        response = requests.get(
            f'{PLAUSIBLE_URL}/api/v1/stats/aggregate',
            headers=get_headers(),
            params={
                'site_id': domaine,
                'period': periode,
                'metrics': 'visitors,pageviews,bounce_rate,visit_duration',
            },
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get('results', {})
        return None
    except Exception:
        return None


def get_pages_populaires(domaine, periode='30d'):
    try:
        response = requests.get(
            f'{PLAUSIBLE_URL}/api/v1/stats/breakdown',
            headers=get_headers(),
            params={
                'site_id': domaine,
                'period': periode,
                'property': 'event:page',
                'metrics': 'visitors,pageviews',
                'limit': 10,
            },
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get('results', [])
        return []
    except Exception:
        return []


def get_sources_trafic(domaine, periode='30d'):
    try:
        response = requests.get(
            f'{PLAUSIBLE_URL}/api/v1/stats/breakdown',
            headers=get_headers(),
            params={
                'site_id': domaine,
                'period': periode,
                'property': 'visit:source',
                'metrics': 'visitors',
                'limit': 10,
            },
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get('results', [])
        return []
    except Exception:
        return []


def get_pays(domaine, periode='30d'):
    try:
        response = requests.get(
            f'{PLAUSIBLE_URL}/api/v1/stats/breakdown',
            headers=get_headers(),
            params={
                'site_id': domaine,
                'period': periode,
                'property': 'visit:country',
                'metrics': 'visitors',
                'limit': 10,
            },
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get('results', [])
        return []
    except Exception:
        return []


def get_series_temporelle(domaine, periode='30d'):
    try:
        response = requests.get(
            f'{PLAUSIBLE_URL}/api/v1/stats/timeseries',
            headers=get_headers(),
            params={
                'site_id': domaine,
                'period': periode,
                'metrics': 'visitors,pageviews',
            },
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get('results', [])
        return []
    except Exception:
        return []
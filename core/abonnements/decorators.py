from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def require_plan(*plans_requis):
    """
    Décorateur pour restreindre l'accès selon le plan.
    Usage : @require_plan('pro', 'business')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('connexion')

            try:
                abonnement = request.user.abonnement
                plan_actuel = abonnement.plan.nom
            except Exception:
                plan_actuel = 'gratuit'

            if plan_actuel not in plans_requis:
                messages.warning(
                    request,
                    f"Cette fonctionnalité nécessite un plan {' ou '.join(plans_requis)}."
                )
                return redirect('tarification')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
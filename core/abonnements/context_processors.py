def plan_utilisateur(request):
    """Rend le plan disponible dans tous les templates"""
    if request.user.is_authenticated:
        try:
            plan = request.user.abonnement.plan.nom
        except Exception:
            plan = 'gratuit'
        return {
            'plan_actuel': plan,
            'est_pro': plan in ['pro', 'business'],
            'est_business': plan == 'business',
        }
    return {
        'plan_actuel': 'gratuit',
        'est_pro': False,
        'est_business': False,
    }
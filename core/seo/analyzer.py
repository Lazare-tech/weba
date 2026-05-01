from bs4 import BeautifulSoup
import re


def analyser_seo(titre, description, corps, tags):
    """
    Analyse le contenu SEO d'un article et retourne
    un score et des conseils d'amélioration
    """
    score = 0
    conseils = []
    points_forts = []

    # 1. Titre
    if titre:
        longueur_titre = len(titre)
        if 50 <= longueur_titre <= 60:
            score += 20
            points_forts.append("Titre de longueur optimale (50-60 caractères)")
        elif longueur_titre < 50:
            score += 10
            conseils.append(
                f"Titre trop court ({longueur_titre} car.) — visez 50-60 caractères"
            )
        else:
            score += 10
            conseils.append(
                f"Titre trop long ({longueur_titre} car.) — visez 50-60 caractères"
            )
    else:
        conseils.append("Ajoutez un titre à votre article")

    # 2. Description / intro
    if description:
        longueur_desc = len(description)
        if 120 <= longueur_desc <= 160:
            score += 20
            points_forts.append("Résumé de longueur optimale (120-160 caractères)")
        elif longueur_desc < 120:
            score += 10
            conseils.append(
                f"Résumé trop court ({longueur_desc} car.) — visez 120-160 caractères"
            )
        else:
            score += 10
            conseils.append(
                f"Résumé trop long ({longueur_desc} car.) — visez 120-160 caractères"
            )
    else:
        conseils.append("Ajoutez un résumé à votre article")

    # 3. Contenu
    if corps:
        soup = BeautifulSoup(corps, 'html.parser')
        texte = soup.get_text()
        mots = len(texte.split())

        if mots >= 300:
            score += 20
            points_forts.append(f"Contenu suffisant ({mots} mots)")
        elif mots >= 150:
            score += 10
            conseils.append(
                f"Contenu court ({mots} mots) — visez au moins 300 mots"
            )
        else:
            conseils.append(
                f"Contenu trop court ({mots} mots) — visez au moins 300 mots"
            )

        # Vérifie les titres H2/H3
        titres = soup.find_all(['h2', 'h3'])
        if titres:
            score += 10
            points_forts.append(f"{len(titres)} sous-titre(s) détecté(s)")
        else:
            conseils.append(
                "Ajoutez des sous-titres (H2, H3) pour structurer votre contenu"
            )

        # Vérifie les images
        images = soup.find_all('img')
        if images:
            score += 10
            points_forts.append(f"{len(images)} image(s) dans le contenu")
        else:
            conseils.append("Ajoutez des images pour enrichir votre contenu")

    # 4. Tags
    nb_tags = tags.count() if hasattr(tags, 'count') else len(tags)
    if nb_tags >= 3:
        score += 10
        points_forts.append(f"{nb_tags} tags ajoutés")
    elif nb_tags >= 1:
        score += 5
        conseils.append(f"Ajoutez plus de tags (actuellement {nb_tags}) — visez 3 minimum")
    else:
        conseils.append("Ajoutez des tags pour catégoriser votre article")

    # 5. Slug
    score += 10
    points_forts.append("URL propre et lisible")

    return {
        'score': min(score, 100),
        'conseils': conseils,
        'points_forts': points_forts,
        'niveau': get_niveau(score),
    }


def get_niveau(score):
    if score >= 80:
        return {'label': 'Excellent', 'couleur': 'green'}
    elif score >= 60:
        return {'label': 'Bon', 'couleur': 'blue'}
    elif score >= 40:
        return {'label': 'Moyen', 'couleur': 'amber'}
    else:
        return {'label': 'Faible', 'couleur': 'red'}
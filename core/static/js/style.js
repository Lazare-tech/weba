// On attend que le DOM soit totalement chargé
document.addEventListener('DOMContentLoaded', function() {
    
    // Sélection des éléments avec précaution
    const newsletterForm = document.getElementById('newsletter-form');
    const newsletterBtn = document.querySelector('#newsletter-form button[type="submit"]');

    // PROTECTION : On n'exécute la logique que si le formulaire existe sur la page actuelle
    if (newsletterForm && newsletterBtn) {
        
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const btnText = newsletterBtn.innerText;

            // État de chargement (Feedback visuel)
            newsletterBtn.disabled = true;
            newsletterBtn.innerHTML = '<span class="flex items-center gap-2"><svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">...</svg> Patientez...</span>';

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
    // 1. On supprime l'alerte
    // alert(data.message); <--- C'est cette ligne qu'il fallait supprimer

    // 2. On affiche le message dans la page
    const messageContainer = document.getElementById('newsletter-status');
    if (messageContainer) {
        messageContainer.innerText = data.message;
        messageContainer.classList.remove('hidden');
        
        // Couleur selon le succès ou l'erreur
        if (data.status === 'success') {
            messageContainer.className = "mt-4 text-sm font-bold text-white bg-white/20 p-3 rounded-lg";
            newsletterForm.reset();
        } else {
            messageContainer.className = "mt-4 text-sm font-bold text-yellow-300";
        }

        // Optionnel : faire disparaître le message après 5 secondes
        setTimeout(() => {
            messageContainer.classList.add('hidden');
        }, 5000);
    }
})
            .catch(error => {
                console.error('Erreur:', error);
            })
            .finally(() => {
                newsletterBtn.disabled = false;
                newsletterBtn.innerText = btnText;
            });
        });
    }
});
///////
  // Initialisation de Lucide (si tu l'utilises)
        lucide.createIcons();

        // Configuration CSRF pour HTMX
        document.body.addEventListener('htmx:configRequest', function(evt) {
            evt.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
        });

        // Fonction de prévisualisation
        function previewImage(input, previewId) {
            const previewContainer = document.getElementById(previewId);
            const file = input.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewContainer.innerHTML = `
                        <img src="${e.target.result}" 
                             class="w-full h-full rounded-lg object-cover border-2 border-emerald-500 shadow-md animate-in zoom-in duration-300">
                    `;
                }
                reader.readAsDataURL(file);
            }
        }

        // Fonction de suppression UNIFIÉE
            function confirmerSuppression(btn) {
    const url = btn.getAttribute('data-url');
    const target = btn.getAttribute('data-target');
    const titre = btn.getAttribute('data-titre') || 'cet élément';

    Swal.fire({
        title: `Supprimer ${titre} ?`,
        text: "Cette action est irréversible.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        confirmButtonText: 'Oui, supprimer',
        cancelButtonText: 'Annuler',
        customClass: {
            popup: 'rounded-[2.5rem] border-none shadow-2xl',
            confirmButton: 'rounded-xl font-bold px-6 py-3',
            cancelButton: 'rounded-xl font-bold px-6 py-3'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            htmx.ajax('DELETE', url, {
                target: target,
                swap: 'outerHTML'
            });

            Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
            }).fire({
                icon: 'success',
                title: 'Supprimé avec succès'
            });
        }
    });
}
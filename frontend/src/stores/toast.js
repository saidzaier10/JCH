import { defineStore } from 'pinia'

export const useToastStore = defineStore('toast', {
    state: () => ({
        toasts: []
    }),
    actions: {
        /**
         * Ajoute une notification.
         * @param {string} message - Le texte à afficher.
         * @param {string} type - Le type de notif (info, success, error).
         * @param {number} duration - Durée en ms avant disparition automatique.
         */
        add(message, type = 'info', duration = 3000) {
            const id = Date.now()
            this.toasts.push({ id, message, type })

            if (duration > 0) {
                setTimeout(() => {
                    this.remove(id)
                }, duration)
            }
        },
        remove(id) {
            this.toasts = this.toasts.filter(t => t.id !== id)
        },
        // Raccourci pour succès
        success(message) {
            this.add(message, 'success')
        },
        // Raccourci pour erreur
        error(message) {
            this.add(message, 'error')
        }
    }
})

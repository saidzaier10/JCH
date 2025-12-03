<template>
    <div :class="[
        'bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden',
        hover ? 'transition-all duration-300 hover:shadow-md hover:-translate-y-1' : '',
        glass ? 'bg-white/80 backdrop-blur-md border-white/20' : '',
        customClass
    ]">
        <div v-if="$slots.header" class="px-6 py-4 border-b border-gray-100 bg-gray-50/50">
            <slot name="header"></slot>
        </div>
        <div class="p-6">
            <slot></slot>
        </div>
        <div v-if="$slots.footer" class="px-6 py-4 border-t border-gray-100 bg-gray-50/50">
            <slot name="footer"></slot>
        </div>
    </div>
</template>

<script setup>
/**
 * Carte de base pour afficher du contenu avec en-tête et pied de page optionnels.
 * Supporte les effets de survol et le style glassmorphism.
 * 
 * @displayName BaseCard
 * 
 * @slot header - Contenu de l'en-tête
 * @slot default - Contenu principal
 * @slot footer - Contenu du pied de page
 */
defineProps({
    hover: {
        type: Boolean,
        default: false
    },
    glass: {
        type: Boolean,
        default: false
    },
    customClass: {
        type: String,
        default: ''
    }
})
</script>

<template>
    <button :type="type" :class="[
        'inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed',
        variantClasses[variant],
        sizeClasses[size],
        rounded ? 'rounded-full' : 'rounded-md',
        block ? 'w-full' : '',
        customClass
    ]" :disabled="disabled || loading" @click="$emit('click')" :aria-busy="loading">
        <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 24 24" aria-hidden="true">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
            </path>
        </svg>
        <span v-if="$slots.icon" class="mr-2">
            <slot name="icon"></slot>
        </span>
        <slot></slot>
    </button>
</template>

<script setup>
import { computed } from 'vue'

/**
 * Bouton de base réutilisable avec différentes variantes et tailles.
 * 
 * @displayName BaseButton
 * 
 * @slot default - Le contenu du bouton (texte)
 * @slot icon - Icône optionnelle à gauche du texte
 */
const props = defineProps({
    type: {
        type: String,
        default: 'button'
    },
    variant: {
        type: String,
        default: 'primary',
        validator: (value) => ['primary', 'secondary', 'danger', 'ghost', 'white'].includes(value)
    },
    size: {
        type: String,
        default: 'md',
        validator: (value) => ['sm', 'md', 'lg'].includes(value)
    },
    loading: {
        type: Boolean,
        default: false
    },
    disabled: {
        type: Boolean,
        default: false
    },
    block: {
        type: Boolean,
        default: false
    },
    rounded: {
        type: Boolean,
        default: false
    },
    customClass: {
        type: String,
        default: ''
    }
})

const variantClasses = {
    primary: 'bg-judo-blue hover:bg-judo-blue-light text-white focus:ring-judo-blue shadow-md hover:shadow-lg',
    secondary: 'bg-gray-100 hover:bg-gray-200 text-gray-800 focus:ring-gray-500',
    danger: 'bg-judo-red hover:bg-judo-red-light text-white focus:ring-judo-red shadow-md hover:shadow-lg',
    ghost: 'bg-transparent hover:bg-gray-100 text-gray-600 hover:text-gray-900',
    white: 'bg-white text-judo-blue hover:bg-gray-50 border border-gray-200 shadow-sm'
}

const sizeClasses = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base'
}
</script>

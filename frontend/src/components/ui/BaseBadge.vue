<template>
    <span :class="[
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
        variantClasses[variant]
    ]">
        <slot></slot>
    </span>
</template>

<script setup>
/**
 * Badge pour afficher des statuts ou des étiquettes.
 * 
 * @displayName BaseBadge
 * 
 * @slot default - Le texte du badge
 */
const props = defineProps({
    variant: {
        type: String,
        default: 'gray',
        validator: (value) => ['gray', 'red', 'green', 'blue', 'yellow', 'indigo', 'purple', 'pink'].includes(value)
    }
})

const variantClasses = {
    gray: 'bg-gray-100 text-gray-800',
    red: 'bg-red-100 text-red-800',
    green: 'bg-green-100 text-green-800',
    blue: 'bg-blue-100 text-blue-800',
    yellow: 'bg-yellow-100 text-yellow-800',
    indigo: 'bg-indigo-100 text-indigo-800',
    purple: 'bg-purple-100 text-purple-800',
    pink: 'bg-pink-100 text-pink-800'
}
</script>

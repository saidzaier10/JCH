<template>
    <div :class="[
        'rounded-2xl overflow-hidden',
        variant === 'glass' ? 'bg-white/10 backdrop-blur-lg border border-white/20 shadow-2xl' : 'bg-white shadow-lg border border-gray-100',
        customClass
    ]">
        <div v-if="$slots.header || title" :class="[
            'px-6 py-4 border-b',
            variant === 'glass' ? 'border-white/10' : 'border-gray-100'
        ]">
            <slot name="header">
                <h3 :class="[
                    'text-lg font-bold',
                    variant === 'glass' ? 'text-white' : 'text-gray-900'
                ]">{{ title }}</h3>
            </slot>
        </div>
        <div class="px-6 py-6">
            <slot></slot>
        </div>
        <div v-if="$slots.footer" :class="[
            'px-6 py-4 bg-gray-50 border-t',
            variant === 'glass' ? 'bg-white/5 border-white/10' : 'bg-gray-50 border-gray-100'
        ]">
            <slot name="footer"></slot>
        </div>
    </div>
</template>

<script setup>
defineProps({
    title: {
        type: String,
        default: ''
    },
    variant: {
        type: String,
        default: 'default',
        validator: (value) => ['default', 'glass'].includes(value)
    },
    customClass: {
        type: String,
        default: ''
    }
})
</script>

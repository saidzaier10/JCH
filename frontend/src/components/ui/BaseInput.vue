<template>
    <div class="w-full">
        <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700 mb-1">
            {{ label }}
        </label>
        <div class="relative rounded-md shadow-sm">
            <div v-if="$slots.prefix" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <slot name="prefix"></slot>
            </div>
            <input :id="id" :type="type" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"
                :placeholder="placeholder" :disabled="disabled" :required="required" v-bind="$attrs" 
                :aria-invalid="!!error"
                :aria-describedby="[error ? `${id}-error` : '', hint ? `${id}-hint` : ''].filter(Boolean).join(' ') || undefined"
                :class="[
                    'block w-full rounded-lg border-gray-300 bg-white focus:bg-white focus:ring-2 focus:ring-judo-blue focus:border-judo-blue sm:text-sm transition-all duration-200 py-3',
                    $slots.prefix ? 'pl-10' : 'pl-4',
                    error ? 'border-red-300 text-red-900 placeholder-red-300 focus:ring-red-500 focus:border-red-500' : '',
                    disabled ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : ''
                ]" />
        </div>
        <p v-if="error" :id="`${id}-error`" class="mt-1 text-sm text-red-600">{{ error }}</p>
        <p v-if="hint" :id="`${id}-hint`" class="mt-1 text-sm text-gray-500">{{ hint }}</p>
    </div>
</template>

<script setup>
defineOptions({
    inheritAttrs: false
})

/**
 * Champ de saisie de texte générique avec label, gestion d'erreur et slots.
 * 
 * @displayName BaseInput
 * 
 * @slot prefix - Élément à afficher au début du champ (ex: icône)
 */
defineProps({
    id: {
        type: String,
        required: true
    },
    label: {
        type: String,
        default: ''
    },
    modelValue: {
        type: [String, Number],
        default: ''
    },
    type: {
        type: String,
        default: 'text'
    },
    placeholder: {
        type: String,
        default: ''
    },
    error: {
        type: String,
        default: ''
    },
    hint: {
        type: String,
        default: ''
    },
    required: {
        type: Boolean,
        default: false
    },
    disabled: {
        type: Boolean,
        default: false
    }
})

defineEmits(['update:modelValue'])
</script>

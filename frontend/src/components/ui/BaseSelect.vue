<template>
    <div class="w-full">
        <label v-if="label" :for="id" class="block text-sm font-medium mb-1"
            :class="variant === 'glass' ? 'text-white' : 'text-gray-700'">
            {{ label }}
        </label>
        <div class="relative rounded-md shadow-sm">
            <select :id="id" :value="modelValue" @change="$emit('update:modelValue', $event.target.value)"
                :disabled="disabled" :required="required" v-bind="$attrs" :class="[
                    'block w-full rounded-xl transition-all duration-200 py-3 appearance-none sm:text-sm',
                    variant === 'glass'
                        ? 'bg-white/10 border-white/20 text-white focus:bg-white/20 focus:ring-2 focus:ring-white/50 focus:border-white/30 backdrop-blur-md'
                        : 'bg-white border-gray-300 text-gray-900 focus:bg-white focus:ring-2 focus:ring-judo-blue focus:border-judo-blue shadow-sm border',
                    error
                        ? (variant === 'glass' ? 'border-red-400 focus:ring-red-400' : 'border-red-300 text-red-900 focus:ring-red-500 focus:border-red-500')
                        : '',
                    disabled ? 'opacity-60 cursor-not-allowed' : ''
                ]">
                <slot></slot>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4"
                :class="variant === 'glass' ? 'text-white' : 'text-gray-500'">
                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                    <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                </svg>
            </div>
        </div>
        <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
        <p v-if="hint" class="mt-1 text-sm text-gray-500">{{ hint }}</p>
    </div>
</template>

<script setup>
defineOptions({
    inheritAttrs: false
})

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
    variant: {
        type: String,
        default: 'default',
        validator: (value) => ['default', 'glass'].includes(value)
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

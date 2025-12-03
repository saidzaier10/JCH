<template>
    <div :class="['animate-pulse bg-gray-200 rounded', className]" :style="{ width: width, height: height }"></div>
</template>

<script setup>
defineProps({
    width: {
        type: String,
        default: '100%'
    },
    height: {
        type: String,
        default: '1rem' // Default text line height
    },
    className: {
        type: String,
        default: ''
    }
});
</script>

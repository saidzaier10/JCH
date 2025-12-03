<script setup>
/**
 * Composant carte pour afficher une fonctionnalité ou un service.
 * @props {Object} icon - Composant icône Lucide
 * @props {String} title - Titre de la carte
 * @props {String} description - Description détaillée
 */
defineProps({
  icon: {
    type: Object,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="bg-white p-8 rounded-sm shadow-lg hover:shadow-xl transition duration-300 border-t-4 border-transparent hover:border-judo-red group">
    <div class="bg-gray-100 w-16 h-16 rounded-full flex items-center justify-center mb-6 text-judo-blue group-hover:bg-judo-blue group-hover:text-white transition duration-300" aria-hidden="true">
      <component :is="icon" class="h-8 w-8" />
    </div>
    <h3 class="text-2xl font-bold text-judo-blue mb-4 uppercase tracking-tight">{{ title }}</h3>
    <p class="text-gray-600 leading-relaxed">
      {{ description }}
    </p>
  </div>
</template>

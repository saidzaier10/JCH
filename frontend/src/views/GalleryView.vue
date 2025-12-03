<script setup>
import { ref, onMounted, computed } from 'vue'
import { Filter } from 'lucide-vue-next'
import api from '@/utils/axios'

const images = ref([])
const loading = ref(true)
const error = ref(null)
const selectedCategory = ref('ALL')

const categories = [
  { id: 'ALL', label: 'Tout' },
  { id: 'EVENT', label: 'Événements' },
  { id: 'COMPETITION', label: 'Compétitions' },
  { id: 'INTERNSHIP', label: 'Stages' },
  { id: 'OTHER', label: 'Autre' }
]

const fetchImages = async () => {
  try {
    const response = await api.get('/api/gallery/')
    images.value = response.data
  } catch (err) {
    error.value = "Impossible de charger la galerie. Veuillez réessayer plus tard."
    console.error(err)
  } finally {
    loading.value = false
  }
}

const filteredImages = computed(() => {
  if (selectedCategory.value === 'ALL') {
    return images.value
  }
  return images.value.filter(img => img.category === selectedCategory.value)
})

onMounted(() => {
  fetchImages()
})
</script>

<template>
  <div class="container mx-auto px-4 py-12">
    <div class="text-center mb-12">
      <h1 class="section-title">Galerie Photos</h1>
      <div class="w-24 h-1 bg-judo-red mx-auto"></div>
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap justify-center gap-4 mb-12">
      <button v-for="category in categories" :key="category.id" @click="selectedCategory = category.id" :class="[
        'px-6 py-2 rounded-sm font-bold uppercase text-sm tracking-wider transition duration-300',
        selectedCategory === category.id
          ? 'bg-judo-red text-white shadow-md'
          : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200 hover:text-judo-blue'
      ]">
        {{ category.label }}
      </button>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-judo-blue mx-auto"></div>
    </div>

    <div v-else-if="error" class="text-center text-red-600 py-12">
      {{ error }}
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div v-for="image in filteredImages" :key="image.id"
        class="group relative overflow-hidden rounded-xl shadow-lg aspect-w-4 aspect-h-3">
        <img :src="image.image" :alt="image.title"
          class="object-cover w-full h-full transform group-hover:scale-110 transition duration-500" />
        <div
          class="absolute inset-0 bg-linear-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-6">
          <h3 class="text-white font-bold text-lg">{{ image.title }}</h3>
        </div>
      </div>
    </div>

    <div v-if="!loading && filteredImages.length === 0" class="text-center text-gray-500 py-12">
      Aucune photo dans cette catégorie pour le moment.
    </div>
  </div>
</template>

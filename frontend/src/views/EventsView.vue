<script setup>
import { ref, onMounted } from 'vue'
import { Calendar, MapPin, Clock } from 'lucide-vue-next'
import api from '@/utils/axios'

const events = ref([])
const loading = ref(true)
const error = ref(null)

const fetchEvents = async () => {
  try {
    const response = await api.get('/api/events/')
    events.value = response.data
  } catch (err) {
    error.value = "Impossible de charger les événements. Veuillez réessayer plus tard."
    console.error(err)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('fr-FR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchEvents()
})
</script>

<template>
  <div class="container mx-auto px-4 py-12">
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-judo-blue uppercase tracking-wide mb-4">Calendrier des Événements</h1>
      <div class="w-24 h-1 bg-judo-red mx-auto"></div>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-judo-blue mx-auto"></div>
    </div>

    <div v-else-if="error" class="text-center text-red-600 py-12">
      {{ error }}
    </div>

    <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div v-for="event in events" :key="event.id"
        class="bg-white rounded-sm shadow-md overflow-hidden hover:shadow-xl transition duration-300 border border-gray-100 flex flex-col group">
        <div class="bg-judo-blue p-4 border-l-4 border-judo-red">
          <h3 class="text-xl font-bold text-white truncate uppercase tracking-wide">{{ event.title }}</h3>
        </div>
        <div class="p-6 grow">
          <div class="space-y-4 mb-6">
            <div class="flex items-start text-gray-600">
              <Calendar class="h-5 w-5 mr-3 mt-0.5 shrink-0 text-judo-red" />
              <span class="font-medium">{{ formatDate(event.start_time) }}</span>
            </div>
            <div class="flex items-start text-gray-600">
              <Clock class="h-5 w-5 mr-3 mt-0.5 shrink-0 text-judo-red" />
              <span>Fin : {{ formatDate(event.end_time) }}</span>
            </div>
            <div v-if="event.location" class="flex items-start text-gray-600">
              <MapPin class="h-5 w-5 mr-3 mt-0.5 shrink-0 text-judo-red" />
              <span>{{ event.location }}</span>
            </div>
          </div>
          <p class="text-gray-600 line-clamp-3">{{ event.description }}</p>
        </div>
        <div class="px-6 pb-6 mt-auto">
          <button
            class="w-full bg-gray-50 text-judo-blue font-bold py-3 rounded-sm hover:bg-judo-blue hover:text-white transition border border-gray-200 uppercase text-sm tracking-wider">
            Voir les détails
          </button>
        </div>
      </div>
    </div>

    <div v-if="!loading && events.length === 0" class="text-center text-gray-500 py-12">
      Aucun événement prévu pour le moment.
    </div>
  </div>
</template>

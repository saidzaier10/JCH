<template>
    <div class="bg-white shadow rounded-lg p-6">
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-bold text-gray-800">Événements</h2>
            <button @click="showCreateModal = true" class="bg-judo-blue text-white px-4 py-2 rounded hover:bg-blue-700">
                + Nouvel Événement
            </button>
        </div>

        <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Titre
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Lieu
                        </th>
                        <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Actions</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="event in events" :key="event.id">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ event.title }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="{
                                'bg-green-100 text-green-800': event.type === 'COMPETITION',
                                'bg-blue-100 text-blue-800': event.type === 'TRAINING',
                                'bg-gray-100 text-gray-800': event.type === 'OTHER'
                            }">
                                {{ event.type }}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {{ new Date(event.start_time).toLocaleDateString() }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ event.location }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                            <button @click="$emit('manage-convocations', event)"
                                class="text-indigo-600 hover:text-indigo-900 mr-4">Convocations</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Create Modal -->
        <div v-if="showCreateModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title"
            role="dialog" aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                    @click="showCreateModal = false"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div
                    class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-100">
                    <div class="bg-white px-6 pt-6 pb-6">
                        <h3 class="text-xl font-bold text-gray-900 mb-6">Créer un événement</h3>
                        <form @submit.prevent="createEvent" class="space-y-5">
                            <BaseInput v-model="newEvent.title" label="Titre" required />

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
                                <select v-model="newEvent.type"
                                    class="w-full rounded-lg border-gray-300 shadow-sm focus:border-judo-blue focus:ring focus:ring-judo-blue focus:ring-opacity-50 border p-3 bg-white">
                                    <option value="COMPETITION">Compétition</option>
                                    <option value="TRAINING">Stage</option>
                                    <option value="OTHER">Autre</option>
                                </select>
                            </div>

                            <div class="grid grid-cols-2 gap-4">
                                <BaseInput v-model="newEvent.start_time" type="datetime-local" label="Date de début"
                                    required />
                                <BaseInput v-model="newEvent.end_time" type="datetime-local" label="Date de fin"
                                    required />
                            </div>

                            <BaseInput v-model="newEvent.location" label="Lieu" />

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                                <textarea v-model="newEvent.description" rows="3"
                                    class="w-full rounded-lg border-gray-300 shadow-sm focus:border-judo-blue focus:ring focus:ring-judo-blue focus:ring-opacity-50 border p-3"></textarea>
                            </div>

                            <div
                                class="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-3 space-y-3 space-y-reverse sm:space-y-0 mt-6">
                                <BaseButton type="button" variant="white" @click="showCreateModal = false"
                                    class="w-full sm:w-auto">
                                    Annuler
                                </BaseButton>
                                <BaseButton type="submit" variant="primary" class="w-full sm:w-auto">
                                    Créer
                                </BaseButton>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/axios'
import BaseButton from './ui/BaseButton.vue'
import BaseInput from './ui/BaseInput.vue'

const events = ref([])
const showCreateModal = ref(false)
const newEvent = ref({
    title: '',
    type: 'COMPETITION',
    start_time: '',
    end_time: '',
    location: '',
    description: ''
})

const fetchEvents = async () => {
    try {
        const res = await api.get('/api/events/')
        events.value = res.data.results || res.data
    } catch (e) {
        console.error(e)
    }
}

const createEvent = async () => {
    try {
        await api.post('/api/events/', newEvent.value)
        showCreateModal.value = false
        newEvent.value = { title: '', type: 'COMPETITION', start_time: '', end_time: '', location: '', description: '' }
        fetchEvents()
    } catch (e) {
        console.error(e)
        alert("Erreur lors de la création")
    }
}

onMounted(fetchEvents)
</script>

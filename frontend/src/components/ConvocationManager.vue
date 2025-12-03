<template>
    <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center justify-between mb-6">
            <div>
                <button @click="$emit('back')" class="text-gray-500 hover:text-gray-700 mb-2 flex items-center">
                    <span class="mr-1">&larr;</span> Retour
                </button>
                <h2 class="text-xl font-bold text-gray-800">Gérer les convocations : {{ event.title }}</h2>
                <p class="text-sm text-gray-500">{{ new Date(event.start_time).toLocaleDateString() }} - {{
                    event.location }}</p>
            </div>
        </div>

        <div class="mb-6 flex space-x-4">
            <div class="w-1/3">
                <label class="block text-sm font-medium text-gray-700 mb-1">Filtrer par catégorie</label>
                <select v-model="selectedCategory"
                    class="w-full rounded-lg border-gray-300 shadow-sm focus:border-judo-blue focus:ring focus:ring-judo-blue focus:ring-opacity-50 border p-3 bg-white">
                    <option value="">Toutes les catégories</option>
                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                </select>
            </div>
        </div>

        <div class="mb-4 flex justify-between items-center">
            <span class="text-sm text-gray-600">{{ selectedMembers.length }} adhérents sélectionnés</span>
            <BaseButton @click="sendConvocations" :disabled="selectedMembers.length === 0 || sending" variant="primary"
                :loading="sending">
                Envoyer les convocations
            </BaseButton>
        </div>

        <div class="overflow-x-auto max-h-96 overflow-y-auto border rounded">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50 sticky top-0">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            <input type="checkbox" @change="toggleAll" :checked="allSelected">
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nom
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Catégorie (Age)</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Statut Convocation</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="member in filteredMembers" :key="member.id">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <input type="checkbox" v-model="selectedMembers" :value="member.id">
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {{ member.first_name }} {{ member.last_name }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {{ getMemberCategory(member) }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            <span v-if="getConvocationStatus(member)"
                                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                {{ getConvocationStatus(member) }}
                            </span>
                            <span v-else class="text-gray-400">-</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '@/utils/axios'
import BaseButton from './ui/BaseButton.vue'

const props = defineProps(['event'])
const emit = defineEmits(['back'])

const members = ref([])
const categories = ref([])
const convocations = ref([])
const selectedCategory = ref('')
const selectedMembers = ref([])
const sending = ref(false)

const fetchData = async () => {
    try {
        const token = localStorage.getItem('access_token')
        const headers = { Authorization: `Bearer ${token}` }

        const [membersRes, categoriesRes, convocationsRes] = await Promise.all([
            api.get('/api/members/'),
            api.get('/api/categories/'),
            api.get(`/api/events/${props.event.id}/convocations/`).catch(() => ({ data: [] })) // Assuming endpoint exists or we fetch all
        ])

        members.value = membersRes.data
        categories.value = categoriesRes.data
        // Note: We haven't implemented GET convocations for an event specifically yet, 
        // but for now let's assume we can't see status or we implement it later.
        // To keep it simple, we won't show status yet or we'll fetch it if we add the endpoint.
    } catch (e) {
        console.error(e)
    }
}

const getMemberCategory = (member) => {
    // Simple estimation based on age logic we implemented
    if (!member.birth_date) return 'Inconnu'
    const birthYear = new Date(member.birth_date).getFullYear()
    // Assuming 2025 season start for calculation
    const age = 2025 - birthYear
    const cat = categories.value.find(c => age >= c.age_min && age <= c.age_max)
    return cat ? cat.name : 'Hors catégorie'
}

const filteredMembers = computed(() => {
    if (!selectedCategory.value) return members.value
    // Filter by category logic
    const cat = categories.value.find(c => c.id === selectedCategory.value)
    if (!cat) return members.value

    return members.value.filter(m => {
        if (!m.birth_date) return false
        const age = 2025 - new Date(m.birth_date).getFullYear()
        return age >= cat.age_min && age <= cat.age_max
    })
})

const allSelected = computed(() => {
    return filteredMembers.value.length > 0 && selectedMembers.value.length === filteredMembers.value.length
})

const toggleAll = () => {
    if (allSelected.value) {
        selectedMembers.value = []
    } else {
        selectedMembers.value = filteredMembers.value.map(m => m.id)
    }
}

const getConvocationStatus = (member) => {
    // Placeholder
    return null
}

const sendConvocations = async () => {
    sending.value = true
    try {
        const token = localStorage.getItem('access_token')
        await api.post('/api/convocations/send/', {
            event_id: props.event.id,
            member_ids: selectedMembers.value
        })
        alert('Convocations envoyées avec succès !')
        selectedMembers.value = []
    } catch (e) {
        console.error(e)
        alert("Erreur lors de l'envoi")
    } finally {
        sending.value = false
    }
}

onMounted(fetchData)
</script>

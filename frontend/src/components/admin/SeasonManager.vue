<script setup>
import { ref, onMounted } from 'vue'
import { Calendar, Plus, Edit, Trash2 } from 'lucide-vue-next'
import BaseCard from '../ui/BaseCard.vue'
import BaseButton from '../ui/BaseButton.vue'
import BaseInput from '../ui/BaseInput.vue'
import api from '@/utils/axios'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()

// State
const seasons = ref([])
const categories = ref([])
const registrations = ref([]) // Needed for counts
const loading = ref(false)

// Modals
const showSeasonModal = ref(false)
const showCategoryModal = ref(false)
const editingSeason = ref(null)
const editingCategory = ref(null)

// Forms
const seasonForm = ref({
    name: '',
    start_date: '',
    end_date: '',
    is_active: false
})

const categoryForm = ref({
    name: '',
    code: '',
    price: 0,
    age_min: 0,
    age_max: 0
})

// Methods
const fetchSeasons = async () => {
    try {
        const res = await api.get('/api/seasons/')
        seasons.value = res.data
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors du chargement des saisons")
    }
}

const fetchCategories = async () => {
    try {
        const res = await api.get('/api/categories/')
        categories.value = res.data
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors du chargement des catégories")
    }
}

const fetchRegistrations = async () => {
    try {
        const res = await api.get('/api/registrations/')
        registrations.value = res.data
    } catch (e) {
        console.error(e)
    }
}

const getCategoryCount = (categoryId) => {
    return registrations.value.filter(r => r.category.id === categoryId).length
}

// Season Logic
const openSeasonModal = (season = null) => {
    if (season) {
        editingSeason.value = season
        seasonForm.value = {
            name: season.name,
            start_date: season.start_date,
            end_date: season.end_date,
            is_active: season.is_active
        }
    } else {
        editingSeason.value = null
        seasonForm.value = {
            name: '',
            start_date: '',
            end_date: '',
            is_active: false
        }
    }
    showSeasonModal.value = true
}

const saveSeason = async () => {
    try {
        if (editingSeason.value) {
            await api.patch(`/api/seasons/${editingSeason.value.id}/`, seasonForm.value)
            toast.success("Saison mise à jour")
        } else {
            await api.post('/api/seasons/', seasonForm.value)
            toast.success("Saison créée")
        }
        showSeasonModal.value = false
        await fetchSeasons()
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de l'enregistrement")
    }
}

const toggleSeasonStatus = async (season) => {
    try {
        await api.patch(`/api/seasons/${season.id}/`, { is_active: !season.is_active })
        toast.success("Statut mis à jour")
        await fetchSeasons()
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de la mise à jour")
    }
}

// Category Logic
const openCategoryModal = (cat = null) => {
    if (cat) {
        editingCategory.value = cat
        categoryForm.value = {
            name: cat.name,
            code: cat.code,
            price: cat.price,
            age_min: cat.age_min,
            age_max: cat.age_max
        }
    } else {
        editingCategory.value = null
        categoryForm.value = {
            name: '',
            code: '',
            price: 0,
            age_min: 0,
            age_max: 0
        }
    }
    showCategoryModal.value = true
}

const saveCategory = async () => {
    try {
        if (editingCategory.value) {
            await api.patch(`/api/categories/${editingCategory.value.id}/`, categoryForm.value)
            toast.success("Catégorie mise à jour")
        } else {
            await api.post('/api/categories/', categoryForm.value)
            toast.success("Catégorie créée")
        }
        showCategoryModal.value = false
        await fetchCategories()
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de l'enregistrement")
    }
}

const deleteCategory = async (id) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette catégorie ?')) return

    try {
        await api.delete(`/api/categories/${id}/`)
        await fetchCategories()
        toast.success('Catégorie supprimée')
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de la suppression")
    }
}

onMounted(() => {
    fetchSeasons()
    fetchCategories()
    fetchRegistrations()
})
</script>

<template>
    <div>
        <div class="mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Gestion des Saisons & Catégories</h2>
            <p class="text-gray-500">Configuration des saisons et catégories du club</p>
        </div>

        <!-- Seasons Section -->
        <BaseCard class="mb-8">
            <template #header>
                <div class="flex justify-between items-center">
                    <h3 class="text-lg font-bold text-gray-900">Saisons</h3>
                    <BaseButton variant="primary" @click="openSeasonModal()">
                        <template #icon>
                            <Plus :size="18" />
                        </template>
                        Nouvelle Saison
                    </BaseButton>
                </div>
            </template>
            <div class="space-y-4">
                <div v-for="season in seasons" :key="season.id"
                    class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
                    <div class="flex items-center space-x-4">
                        <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                            <Calendar :size="24" class="text-purple-600" />
                        </div>
                        <div>
                            <h4 class="text-lg font-medium text-gray-900">{{ season.name }}</h4>
                            <p class="text-sm text-gray-500">
                                {{ new Date(season.start_date).toLocaleDateString() }} -
                                {{ new Date(season.end_date).toLocaleDateString() }}
                            </p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span v-if="season.is_active"
                            class="px-3 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                            Active
                        </span>
                        <span v-else class="px-3 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800">
                            Inactive
                        </span>
                        <button @click="openSeasonModal(season)"
                            class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition mr-2">
                            <Edit :size="16" />
                        </button>
                        <button @click="toggleSeasonStatus(season)"
                            class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition">
                            {{ season.is_active ? 'Désactiver' : 'Activer' }}
                        </button>
                    </div>
                </div>
            </div>
        </BaseCard>

        <!-- Categories Section -->
        <BaseCard>
            <template #header>
                <div class="flex justify-between items-center">
                    <h3 class="text-lg font-bold text-gray-900">Catégories</h3>
                    <BaseButton variant="primary" @click="openCategoryModal()">
                        <template #icon>
                            <Plus :size="18" />
                        </template>
                        Nouvelle Catégorie
                    </BaseButton>
                </div>
            </template>
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nom</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Code</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Âge</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Prix</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Inscrits</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="cat in categories" :key="cat.id" class="hover:bg-gray-50">
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ cat.name }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ cat.code }}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ cat.age_min }} - {{
                                cat.age_max }}
                                ans</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ cat.price }} €
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                                    {{ getCategoryCount(cat.id) }} membres
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm">
                                <button @click="openCategoryModal(cat)" class="text-blue-600 hover:text-blue-900 mr-3">
                                    <Edit :size="16" />
                                </button>
                                <button @click="deleteCategory(cat.id)" class="text-red-600 hover:text-red-900">
                                    <Trash2 :size="16" />
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </BaseCard>

        <!-- Season Modal -->
        <div v-if="showSeasonModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title"
            role="dialog" aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                    @click="showSeasonModal = false"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div
                    class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-100">
                    <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
                            {{ editingSeason ? 'Modifier la saison' : 'Nouvelle Saison' }}
                        </h3>
                        <form @submit.prevent="saveSeason" class="space-y-4">
                            <BaseInput label="Nom" v-model="seasonForm.name" required placeholder="Ex: 2023-2024" />
                            <div class="grid grid-cols-2 gap-4">
                                <BaseInput label="Date de début" type="date" v-model="seasonForm.start_date" required />
                                <BaseInput label="Date de fin" type="date" v-model="seasonForm.end_date" required />
                            </div>
                            <div class="flex items-center">
                                <input type="checkbox" id="is_active" v-model="seasonForm.is_active"
                                    class="h-4 w-4 text-judo-blue focus:ring-judo-blue border-gray-300 rounded">
                                <label for="is_active" class="ml-2 block text-sm text-gray-900">Saison active</label>
                            </div>
                            <div
                                class="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-3 space-y-3 space-y-reverse sm:space-y-0 mt-6">
                                <BaseButton type="button" variant="white" @click="showSeasonModal = false"
                                    class="w-full sm:w-auto">
                                    Annuler
                                </BaseButton>
                                <BaseButton type="submit" variant="primary" class="w-full sm:w-auto">
                                    Enregistrer
                                </BaseButton>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <!-- Category Modal -->
        <div v-if="showCategoryModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title"
            role="dialog" aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                    @click="showCategoryModal = false"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div
                    class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-100">
                    <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
                            {{ editingCategory ? 'Modifier la catégorie' : 'Nouvelle Catégorie' }}
                        </h3>
                        <form @submit.prevent="saveCategory" class="space-y-4">
                            <BaseInput label="Nom" v-model="categoryForm.name" required placeholder="Ex: Poussins" />
                            <BaseInput label="Code" v-model="categoryForm.code" required placeholder="Ex: PO" />
                            <BaseInput label="Prix" type="number" v-model="categoryForm.price" required />
                            <div class="grid grid-cols-2 gap-4">
                                <BaseInput label="Âge min" type="number" v-model="categoryForm.age_min" required />
                                <BaseInput label="Âge max" type="number" v-model="categoryForm.age_max" required />
                            </div>
                            <div
                                class="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-3 space-y-3 space-y-reverse sm:space-y-0 mt-6">
                                <BaseButton type="button" variant="white" @click="showCategoryModal = false"
                                    class="w-full sm:w-auto">
                                    Annuler
                                </BaseButton>
                                <BaseButton type="submit" variant="primary" class="w-full sm:w-auto">
                                    Enregistrer
                                </BaseButton>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

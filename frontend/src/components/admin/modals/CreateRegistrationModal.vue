<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import api from '@/utils/axios'
import { useToastStore } from '@/stores/toast'

const props = defineProps({
    isOpen: {
        type: Boolean,
        required: true
    }
})

const emit = defineEmits(['close', 'created'])

const toast = useToastStore()
const creating = ref(false)
const loadingData = ref(false)

// Data sources
const members = ref([])
const seasons = ref([])
const categories = ref([])

const form = ref({
    member_id: '',
    season_id: '',
    category_id: '',
    discount_percentage: 0,
    discount_amount: 0,
    has_supplementary_discipline: false,
    city_hall_aid: false,
    city_hall_aid_amount: 0
})

const fetchData = async () => {
    loadingData.value = true
    try {
        const [membersRes, seasonsRes, categoriesRes] = await Promise.all([
            api.get('/api/members/'), // Admin should see all members
            api.get('/api/seasons/active/'), // Or list all seasons? active is safer default
            api.get('/api/categories/')
        ])

        members.value = membersRes.data.results || membersRes.data
        categories.value = categoriesRes.data.results || categoriesRes.data

        // Handle season: if active endpoint returns object directly
        if (seasonsRes.data.id) {
            seasons.value = [seasonsRes.data]
            form.value.season_id = seasonsRes.data.id
        } else {
            // Fallback if list
            seasons.value = seasonsRes.data.results || seasonsRes.data
            const active = seasons.value.find(s => s.is_active)
            if (active) form.value.season_id = active.id
        }

    } catch (e) {
        console.error("Error loading data:", e)
        toast.error("Impossible de charger les données nécessaires")
    } finally {
        loadingData.value = false
    }
}

watch(() => props.isOpen, (newVal) => {
    if (newVal) {
        fetchData()
    }
})

const selectedCategory = computed(() => {
    return categories.value.find(c => c.id === form.value.category_id)
})

const estimatedPrice = computed(() => {
    if (!selectedCategory.value) return 0
    let price = parseFloat(selectedCategory.value.price)

    // Discounts
    if (form.value.discount_amount) price -= parseFloat(form.value.discount_amount)
    if (form.value.discount_percentage) price -= (price * (parseFloat(form.value.discount_percentage) / 100))

    // Additions
    if (form.value.has_supplementary_discipline) price += 40 // Assuming 40 is standard

    // Aid
    if (form.value.city_hall_aid && form.value.city_hall_aid_amount) {
        // Did we implement aid as deduction? In PriceCalculator yes.
        // It's usually a deduction from what user pays, so let's subtract for preview.
        price -= parseFloat(form.value.city_hall_aid_amount)
    }

    return Math.max(0, price).toFixed(2)
})

const create = async () => {
    creating.value = true
    try {
        await api.post('/api/registrations/', form.value)
        toast.success("Inscription créée avec succès")
        emit('created')
        emit('close')
        // Reset (keep season)
        form.value.member_id = ''
        form.value.category_id = ''
        form.value.discount_percentage = 0
        form.value.discount_amount = 0
        form.value.has_supplementary_discipline = false
        form.value.city_hall_aid = false
        form.value.city_hall_aid_amount = 0
    } catch (e) {
        console.error(e)
        // Check for specific error like "Registration already exists"
        const msg = e.response?.data?.non_field_errors?.[0] || e.response?.data?.detail || "Erreur lors de l'inscription"
        toast.error(msg)
    } finally {
        creating.value = false
    }
}
</script>

<template>
    <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog"
        aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                @click="$emit('close')"></div>
            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div
                class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
                        Nouvelle Inscription Manuelle
                    </h3>
                    <form @submit.prevent="create" class="space-y-4">

                        <BaseSelect label="Saison" v-model="form.season_id" required>
                            <option v-for="season in seasons" :key="season.id" :value="season.id">
                                {{ season.name }}
                            </option>
                        </BaseSelect>

                        <BaseSelect label="Membre" v-model="form.member_id" required :disabled="loadingData">
                            <option value="">Sélectionner un membre...</option>
                            <option v-for="member in members" :key="member.id" :value="member.id">
                                {{ member.first_name }} {{ member.last_name }}
                            </option>
                        </BaseSelect>

                        <BaseSelect label="Catégorie" v-model="form.category_id" required>
                            <option value="">Sélectionner une catégorie...</option>
                            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                                {{ cat.name }} ({{ cat.price }} €)
                            </option>
                        </BaseSelect>

                        <div v-if="selectedCategory" class="p-3 bg-gray-50 rounded-lg border border-gray-200">
                            <div class="flex justify-between items-center mb-2">
                                <span class="text-sm font-medium text-gray-700">Prix de base:</span>
                                <span class="font-bold">{{ selectedCategory.price }} €</span>
                            </div>

                            <div class="space-y-3 pt-2 border-t border-gray-200">
                                <BaseInput type="number" v-model="form.discount_amount" label="Remise (€)" step="0.5" />
                                <BaseInput type="number" v-model="form.discount_percentage" label="Remise (%)" step="1"
                                    max="100" />

                                <div class="flex items-center">
                                    <input id="new_reg_supp" v-model="form.has_supplementary_discipline" type="checkbox"
                                        class="h-4 w-4 text-judo-blue focus:ring-judo-blue border-gray-300 rounded">
                                    <label for="new_reg_supp" class="ml-2 block text-sm text-gray-900">
                                        Discipline supplémentaire (+40€)
                                    </label>
                                </div>
                            </div>
                            <div class="mt-3 pt-2 border-t border-gray-200 flex justify-between items-center">
                                <span class="text-sm font-bold text-gray-900">Estimation Total:</span>
                                <span class="text-xl font-bold text-judo-blue">{{ estimatedPrice }} €</span>
                            </div>
                        </div>

                        <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                            <BaseButton type="submit" variant="primary" :loading="creating"
                                class="w-full sm:col-start-2">
                                Créer Inscription
                            </BaseButton>
                            <BaseButton type="button" variant="white" @click="$emit('close')"
                                class="mt-3 w-full sm:mt-0 sm:col-start-1">
                                Annuler
                            </BaseButton>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

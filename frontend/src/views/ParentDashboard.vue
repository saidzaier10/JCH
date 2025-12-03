<template>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex items-center justify-between mb-8">
            <h1 class="text-3xl font-bold text-gray-900">Mon Espace Famille</h1>
            <div class="text-sm text-gray-500">
                Bienvenue, {{ familyData.children.length }} enfant(s) inscrit(s)
            </div>
        </div>

        <div v-if="loading" class="flex justify-center py-20">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-judo-blue"></div>
        </div>

        <div v-else-if="error" class="text-center py-12">
            <div class="bg-red-50 text-red-600 p-4 rounded-lg inline-block">
                {{ error }}
            </div>
        </div>

        <div v-else class="space-y-8">
            <!-- Tabs -->
            <div class="flex space-x-1 bg-white p-1 rounded-xl shadow-sm border border-gray-100 w-fit">
                <button v-for="tab in tabs" :key="tab.id" @click="currentTab = tab.id" :class="[
                    'px-6 py-2.5 text-sm font-medium rounded-lg transition-all duration-200',
                    currentTab === tab.id
                        ? 'bg-judo-blue text-white shadow-md'
                        : 'text-gray-500 hover:text-gray-900 hover:bg-gray-50'
                ]">
                    {{ tab.name }}
                    <span v-if="tab.count" class="ml-2 bg-white/20 text-white py-0.5 px-2 rounded-full text-xs">
                        {{ tab.count }}
                    </span>
                </button>
            </div>

            <!-- Tab: Children -->
            <Transition name="fade" mode="out-in">
                <div v-if="currentTab === 'children'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <BaseCard v-for="child in familyData.children" :key="child.id" hover glass>
                        <div class="flex items-center mb-4">
                            <div
                                class="shrink-0 bg-linear-to-br from-judo-blue to-blue-600 rounded-full h-14 w-14 flex items-center justify-center text-white font-bold text-xl shadow-lg">
                                {{ child.first_name.charAt(0) }}
                            </div>
                            <div class="ml-4">
                                <h3 class="text-lg font-bold text-gray-900">{{ child.first_name }} {{ child.last_name }}
                                </h3>
                                <p class="text-sm text-gray-500">Né(e) le {{ new
                                    Date(child.birth_date).toLocaleDateString() }}</p>
                            </div>
                        </div>
                        <div class="border-t border-gray-100 pt-4 space-y-3">
                            <div class="flex justify-between items-center">
                                <span class="text-sm text-gray-500">Ceinture</span>
                                <BaseBadge variant="blue">{{ child.belt }}</BaseBadge>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="text-sm text-gray-500">Licence</span>
                                <span class="text-sm font-medium text-gray-900">{{ child.license_number || 'En attente'
                                    }}</span>
                            </div>
                            <div class="pt-2 flex justify-end">
                                <button @click.stop="openEditModal(child)"
                                    class="text-sm text-blue-600 hover:text-blue-800 font-medium">
                                    Modifier
                                </button>
                            </div>
                        </div>
                    </BaseCard>
                    <div v-if="familyData.children.length === 0"
                        class="col-span-full text-center py-12 bg-white rounded-xl border border-dashed border-gray-300">
                        <p class="text-gray-500">Aucun enfant inscrit pour le moment.</p>
                        <BaseButton class="mt-4" variant="primary" @click="$router.push('/inscription')">Inscrire un
                            enfant</BaseButton>
                    </div>
                </div>

                <!-- Tab: Convocations -->
                <div v-else-if="currentTab === 'convocations'" class="space-y-4">
                    <BaseCard v-for="convocation in familyData.convocations" :key="convocation.id"
                        class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                        <div class="flex-1">
                            <div class="flex items-center justify-between mb-2">
                                <h3 class="font-bold text-judo-blue text-lg">{{ convocation.event_title }}</h3>
                                <BaseBadge :variant="getStatusVariant(convocation.status_code)">
                                    {{ convocation.status }}
                                </BaseBadge>
                            </div>
                            <div class="flex flex-wrap gap-4 text-sm text-gray-600">
                                <span class="flex items-center">👤 {{ convocation.member_name }}</span>
                                <span class="flex items-center">📅 {{ new
                                    Date(convocation.event_date).toLocaleDateString() }}</span>
                                <span class="flex items-center">📍 {{ convocation.event_location }}</span>
                            </div>
                        </div>
                        <div class="flex space-x-2">
                            <!-- Actions could go here -->
                        </div>
                    </BaseCard>
                    <div v-if="familyData.convocations.length === 0"
                        class="text-center py-12 bg-white rounded-xl border border-dashed border-gray-300">
                        <p class="text-gray-500">Aucune convocation en cours.</p>
                    </div>
                </div>

                <!-- Tab: Documents -->
                <div v-else-if="currentTab === 'documents'" class="space-y-4">
                    <BaseCard v-for="invoice in familyData.invoices" :key="invoice.id"
                        class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                        <div>
                            <div class="flex items-center space-x-3 mb-1">
                                <span class="font-bold text-gray-900">Facture #{{ invoice.id }}</span>
                                <BaseBadge :variant="invoice.paid ? 'green' : 'red'">
                                    {{ invoice.paid ? 'Payée' : 'À payer' }}
                                </BaseBadge>
                            </div>
                            <p class="text-sm text-gray-500">
                                Émise le {{ new Date(invoice.date_issued).toLocaleDateString() }} • Montant : <span
                                    class="font-bold text-gray-900">{{ invoice.amount }} €</span>
                            </p>
                        </div>
                        <div class="flex space-x-3">
                            <BaseButton v-if="!invoice.paid" variant="primary" size="sm"
                                @click="payInvoice(invoice.id)">
                                <template #icon>💳</template>
                                Payer
                            </BaseButton>
                            <BaseButton variant="white" size="sm" @click="downloadInvoice(invoice.id)">
                                <template #icon>📥</template>
                                PDF
                            </BaseButton>
                        </div>
                    </BaseCard>
                    <div v-if="familyData.invoices.length === 0"
                        class="text-center py-12 bg-white rounded-xl border border-dashed border-gray-300">
                        <p class="text-gray-500">Aucun document disponible.</p>
                    </div>
                </div>
            </Transition>
        </div>
        <!-- Edit Child Modal -->
        <div v-if="showEditModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog"
            aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"
                    @click="showEditModal = false"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div
                    class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                    <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
                            Modifier les informations
                        </h3>
                        <form @submit.prevent="updateChild" class="space-y-4">
                            <div class="grid grid-cols-2 gap-4">
                                <BaseInput id="edit-firstname" label="Prénom" v-model="editForm.first_name" required />
                                <BaseInput id="edit-lastname" label="Nom" v-model="editForm.last_name" required />
                            </div>
                            <BaseInput id="edit-birthdate" label="Date de naissance" type="date"
                                v-model="editForm.birth_date" required />

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Catégorie de poids</label>
                                <select v-model="editForm.weight_category"
                                    class="w-full rounded-md border-gray-300 shadow-sm focus:ring-judo-blue focus:border-judo-blue">
                                    <option value="">Sélectionner...</option>
                                    <option v-for="weight in availableWeights" :key="weight.value"
                                        :value="weight.value">
                                        {{ weight.label }}
                                    </option>
                                </select>
                            </div>

                            <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                <BaseButton type="submit" variant="primary" :loading="updating"
                                    class="w-full sm:col-start-2">
                                    Enregistrer
                                </BaseButton>
                                <BaseButton type="button" variant="white" @click="showEditModal = false"
                                    class="mt-3 w-full sm:mt-0 sm:col-start-1">
                                    Annuler
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
import { ref, onMounted, computed } from 'vue'
import api from '@/utils/axios'
import { useToastStore } from '../stores/toast'
import BaseCard from '../components/ui/BaseCard.vue'
import BaseButton from '../components/ui/BaseButton.vue'
import BaseBadge from '../components/ui/BaseBadge.vue'
import BaseInput from '../components/ui/BaseInput.vue'
import { getWeightCategories } from '@/utils/judo-weights'

const currentTab = ref('children')
const loading = ref(true)
const error = ref(null)
const familyData = ref({
    children: [],
    convocations: [],
    invoices: []
})
const toast = useToastStore()

// Edit State
const showEditModal = ref(false)
const updating = ref(false)
const editingChildId = ref(null)
const editForm = ref({
    first_name: '',
    last_name: '',
    birth_date: '',
    gender: 'M',
    weight_category: ''
})

const availableWeights = computed(() => {
    return getWeightCategories(editForm.value.birth_date, editForm.value.gender)
})

const openEditModal = (child) => {
    editingChildId.value = child.id
    editForm.value = {
        first_name: child.first_name,
        last_name: child.last_name,
        birth_date: child.birth_date,
        gender: child.gender,
        weight_category: child.weight_category || ''
    }
    showEditModal.value = true
}

const updateChild = async () => {
    updating.value = true
    try {
        await api.patch(`/api/members/${editingChildId.value}/`, editForm.value)
        toast.success('Informations mises à jour')
        showEditModal.value = false
        await fetchFamilyData()
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de la mise à jour")
    } finally {
        updating.value = false
    }
}

const tabs = computed(() => [
    { id: 'children', name: 'Mes Enfants' },
    { id: 'convocations', name: 'Convocations', count: familyData.value.convocations.length },
    { id: 'documents', name: 'Documents & Factures' }
])

const getStatusVariant = (status) => {
    switch (status) {
        case 'CONFIRMED': return 'green'
        case 'SENT': return 'yellow'
        case 'DECLINED': return 'red'
        default: return 'gray'
    }
}

const fetchFamilyData = async () => {
    try {
        const response = await api.get('/api/my-family/')
        familyData.value = response.data
    } catch (e) {
        console.error(e)
        error.value = "Impossible de charger les données de votre famille."
        toast.error("Erreur de chargement des données.")
    } finally {
        loading.value = false
    }
}

const downloadInvoice = async (invoiceId) => {
    try {
        const response = await api.get(`/api/invoices/${invoiceId}/download/`, {
            responseType: 'blob'
        })

        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `Facture_${invoiceId}.pdf`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        toast.success("Facture téléchargée avec succès !")
    } catch (e) {
        console.error("Erreur téléchargement PDF", e)
        toast.error("Erreur lors du téléchargement de la facture")
    }
}

const payInvoice = async (invoiceId) => {
    try {
        const response = await api.post('/api/payments/create-checkout-session/',
            { invoice_id: invoiceId }
        )

        if (response.data.url) {
            window.location.href = response.data.url
        }
    } catch (e) {
        console.error("Erreur paiement", e)
        toast.error("Erreur lors de l'initialisation du paiement")
    }
}

onMounted(() => {
    fetchFamilyData()
})
</script>

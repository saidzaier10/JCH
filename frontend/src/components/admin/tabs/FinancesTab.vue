<script setup>
import { ref, computed } from 'vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import PaymentModal from '@/components/admin/modals/PaymentModal.vue'
import BulkEmailModal from '@/components/admin/modals/BulkEmailModal.vue'
import PaymentSettingsModal from '@/components/admin/modals/PaymentSettingsModal.vue'
import { Mail, Edit, Settings } from 'lucide-vue-next'
import { useToastStore } from '@/stores/toast'

const props = defineProps({
    registrations: {
        type: Array,
        default: () => []
    },
    financialStats: {
        type: Object,
        default: () => ({ paid_revenue: 0, paid_count: 0, pending_revenue: 0, pending_count: 0 })
    },
    stats: {
        type: Object,
        default: () => ({ total_revenue: 0 })
    },
    paymentRate: {
        type: [Number, String],
        default: 0
    },
    loading: {
        type: Boolean,
        default: false
    },
    allMembers: {
        type: Array, // Needed for email resolution
        default: () => []
    }
})

const emit = defineEmits(['refresh'])

const toast = useToastStore()

// Payment Modal State
const showPaymentModal = ref(false)
const editingPaymentReg = ref(null)

const openPaymentModal = (reg) => {
    editingPaymentReg.value = reg
    showPaymentModal.value = true
}

// Bulk Email State (for reminders)
const showEmailModal = ref(false)
const showSettingsModal = ref(false)
const selectedMembersForEmail = ref([])
const emailForm = ref({
    subject: '',
    body: ''
})

const remindUnpaidMembers = () => {
    const unpaidRegs = props.registrations.filter(r => !r.paid)
    if (unpaidRegs.length === 0) {
        toast.info("Aucun impayé à relancer")
        return
    }
    const unpaidMemberIds = unpaidRegs.map(r => r.member.id)
    selectedMembersForEmail.value = unpaidMemberIds

    // Pre-fill email
    emailForm.value = {
        subject: "Rappel de cotisation - Judo Club",
        body: "Bonjour,\n\nSauf erreur de notre part, nous n'avons pas encore reçu le règlement de votre cotisation pour la saison en cours.\n\nMerci de régulariser votre situation rapidement.\n\nCordialement,\nLe Bureau"
    }
    showEmailModal.value = true
}

const formatCurrency = (value) => {
    const number = parseFloat(value)
    if (isNaN(number)) return '0,00 €'
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(number)
}

// Filtering & Sorting
const currentFilter = ref('all') // 'all', 'paid', 'unpaid', 'partial'
const sortKey = ref('member') // 'member', 'category', 'amount', 'status'
const sortOrder = ref('asc') // 'asc', 'desc'

const filteredRegistrations = computed(() => {
    let result = [...props.registrations]

    // 1. Filter
    if (currentFilter.value === 'paid') {
        result = result.filter(r => r.paid)
    } else if (currentFilter.value === 'unpaid') {
        result = result.filter(r => !r.paid)
    } else if (currentFilter.value === 'partial') {
        result = result.filter(r => !r.paid && r.payment_mode === '3X')
    }

    // 2. Sort
    result.sort((a, b) => {
        let valA, valB

        switch (sortKey.value) {
            case 'member':
                valA = `${a.member.last_name} ${a.member.first_name}`.toLowerCase()
                valB = `${b.member.last_name} ${b.member.first_name}`.toLowerCase()
                break
            case 'category':
                valA = a.category.name.toLowerCase()
                valB = b.category.name.toLowerCase()
                break
            case 'amount':
                valA = parseFloat(a.category.price)
                valB = parseFloat(b.category.price)
                break
            case 'status':
                valA = a.paid ? 1 : 0
                valB = b.paid ? 1 : 0
                break
            default:
                return 0
        }

        if (valA < valB) return sortOrder.value === 'asc' ? -1 : 1
        if (valA > valB) return sortOrder.value === 'asc' ? 1 : -1
        return 0
    })

    return result
})

const selectedSum = computed(() => {
    return filteredRegistrations.value.reduce((sum, r) => sum + parseFloat(r.category.price), 0)
})

const setFilter = (filter) => {
    currentFilter.value = filter
}

const sortBy = (key) => {
    if (sortKey.value === key) {
        sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
    } else {
        sortKey.value = key
        sortOrder.value = 'asc'
    }
}

const onRefresh = () => {
    emit('refresh')
}
</script>

<template>
    <div>
        <div class="mb-6 flex justify-between items-center">
            <div>
                <h2 class="text-2xl font-bold text-gray-900">Gestion Financière</h2>
                <p class="text-gray-500">Suivi des paiements et revenus</p>
            </div>
            <BaseButton variant="white" @click="showSettingsModal = true">
                <template #icon>
                    <Settings :size="20" />
                </template>
                Paramètres
            </BaseButton>
        </div>

        <!-- Financial KPIs -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <BaseCard class="border-l-4 border-l-green-500">
                <h3 class="text-gray-500 text-sm font-medium uppercase tracking-wider">Revenus Perçus</h3>
                <p class="text-3xl font-bold text-gray-900 mt-2">{{ formatCurrency(financialStats.paid_revenue) }}</p>
                <p class="text-xs text-green-600 mt-1">{{ financialStats.paid_count }} paiements</p>
            </BaseCard>
            <BaseCard class="border-l-4 border-l-orange-500">
                <h3 class="text-gray-500 text-sm font-medium uppercase tracking-wider">En Attente</h3>
                <p class="text-3xl font-bold text-gray-900 mt-2">{{ formatCurrency(financialStats.pending_revenue) }}
                </p>
                <p class="text-xs text-orange-600 mt-1">{{ financialStats.pending_count }} impayés</p>
            </BaseCard>
            <BaseCard class="border-l-4 border-l-blue-500">
                <h3 class="text-gray-500 text-sm font-medium uppercase tracking-wider">Revenu Total</h3>
                <p class="text-3xl font-bold text-gray-900 mt-2">{{ formatCurrency(stats?.total_revenue || 0) }}</p>
            </BaseCard>
            <BaseCard class="border-l-4 border-l-purple-500">
                <h3 class="text-gray-500 text-sm font-medium uppercase tracking-wider">Taux de Paiement</h3>
                <p class="text-3xl font-bold text-gray-900 mt-2">{{ paymentRate }}%</p>
            </BaseCard>
        </div>

        <!-- Payments List -->
        <BaseCard>
            <template #header>
                <div class="flex justify-between items-center">
                    <h3 class="text-lg font-bold text-gray-900">Suivi des Paiements</h3>
                    <BaseButton variant="secondary" @click="remindUnpaidMembers">
                        <template #icon>
                            <Mail :size="18" />
                        </template>
                        Relancer les impayés
                    </BaseButton>
                </div>
            </template>
            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-judo-blue"></div>
            </div>
            <div v-else class="overflow-x-auto">
                <div class="p-4 bg-gray-50 border-b border-gray-200 flex justify-between items-center flex-wrap gap-4">
                    <div class="flex space-x-2">
                        <button @click="setFilter('all')" class="px-3 py-1 text-sm rounded-full transition-colors"
                            :class="currentFilter === 'all' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 border hover:bg-gray-50'">
                            Tous
                        </button>
                        <button @click="setFilter('paid')" class="px-3 py-1 text-sm rounded-full transition-colors"
                            :class="currentFilter === 'paid' ? 'bg-green-600 text-white' : 'bg-white text-gray-600 border hover:bg-gray-50'">
                            Payés
                        </button>
                        <button @click="setFilter('unpaid')" class="px-3 py-1 text-sm rounded-full transition-colors"
                            :class="currentFilter === 'unpaid' ? 'bg-orange-500 text-white' : 'bg-white text-gray-600 border hover:bg-gray-50'">
                            Impayés
                        </button>
                        <button @click="setFilter('partial')" class="px-3 py-1 text-sm rounded-full transition-colors"
                            :class="currentFilter === 'partial' ? 'bg-blue-400 text-white' : 'bg-white text-gray-600 border hover:bg-gray-50'">
                            Partiels (3X)
                        </button>
                    </div>
                    <div class="text-sm font-medium text-gray-700">
                        Total affiché: <span class="font-bold">{{ formatCurrency(selectedSum) }}</span>
                        <span class="text-gray-400 mx-2">|</span>
                        {{ filteredRegistrations.length }} inscriptions
                    </div>
                </div>

                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th @click="sortBy('member')"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100">
                                Membre
                                <span v-if="sortKey === 'member'">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
                            </th>
                            <th @click="sortBy('category')"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100">
                                Catégorie
                                <span v-if="sortKey === 'category'">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
                            </th>
                            <th @click="sortBy('amount')"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100">
                                Montant
                                <span v-if="sortKey === 'amount'">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
                            </th>
                            <th @click="sortBy('status')"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100">
                                Statut
                                <span v-if="sortKey === 'status'">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
                            </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="reg in filteredRegistrations" :key="reg.id" class="hover:bg-gray-50">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm font-medium text-gray-900">{{ reg.member.first_name }} {{
                                    reg.member.last_name }}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                                    {{ reg.category.name }}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                {{ reg.category.price }} €
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center justify-between">
                                    <div>
                                        <span v-if="reg.paid"
                                            class="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                                            ✓ Payé
                                        </span>
                                        <span v-else-if="reg.payment_mode === '3X'"
                                            class="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                                            {{ reg.installments_paid }}/3 Payé
                                        </span>
                                        <span v-else
                                            class="px-2 py-1 text-xs font-semibold rounded-full bg-orange-100 text-orange-800">
                                            ⏳ En attente
                                        </span>
                                    </div>
                                    <button @click="openPaymentModal(reg)"
                                        class="text-gray-400 hover:text-judo-blue ml-2">
                                        <Edit :size="16" />
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </BaseCard>

        <!-- Modals -->
        <PaymentModal :is-open="showPaymentModal" :registration="editingPaymentReg" @close="showPaymentModal = false"
            @saved="onRefresh" />

        <BulkEmailModal :is-open="showEmailModal" :selected-members="selectedMembersForEmail" :all-members="allMembers"
            :initial-subject="emailForm.subject" :initial-body="emailForm.body" @close="showEmailModal = false"
            @sent="onRefresh" />

        <PaymentSettingsModal :is-open="showSettingsModal" @close="showSettingsModal = false" />
    </div>
</template>

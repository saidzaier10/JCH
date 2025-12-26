<script setup>
import { ref } from 'vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import EditPriceModal from '@/components/admin/modals/EditPriceModal.vue'
import CreateRegistrationModal from '@/components/admin/modals/CreateRegistrationModal.vue'
import { Plus } from 'lucide-vue-next'

const props = defineProps({
    registrations: {
        type: Array,
        default: () => []
    },
    loading: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['refresh', 'export'])

// Price Modal State
const showPriceModal = ref(false)
const showCreateModal = ref(false)
const editingRegistration = ref(null)

const openPriceModal = (reg) => {
    editingRegistration.value = reg
    showPriceModal.value = true
}

const onRefresh = () => {
    emit('refresh')
}
</script>

<template>
    <div>
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Liste des Inscriptions</h2>
            <div class="flex space-x-3">
                <BaseButton variant="primary" @click="showCreateModal = true">
                    <template #icon>
                        <Plus :size="20" />
                    </template>
                    Ajouter Inscription
                </BaseButton>
                <BaseButton variant="white" @click="$emit('export')">
                    <template #icon>📄</template>
                    Exporter Excel
                </BaseButton>
            </div>
        </div>

        <div v-if="loading" class="flex justify-center py-20">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-judo-blue"></div>
        </div>

        <BaseCard v-else class="overflow-hidden">
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Enfant</th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Parent</th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Contact</th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Catégorie</th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Total
                            </th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Reste à payer
                            </th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Statut</th>
                            <th scope="col" class="relative px-6 py-3">
                                <span class="sr-only">Actions</span>
                            </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="reg in registrations" :key="reg.id" class="hover:bg-gray-50">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm font-medium text-gray-900">{{ reg.member.first_name }} {{
                                    reg.member.last_name }}</div>
                                <div class="text-xs text-gray-500">Né(e) le {{ reg.member.birth_date }}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-gray-900">{{ reg.member.parent_name || 'N/A' }}</div>
                                <div class="text-xs text-gray-500">{{ reg.member.parent_email || 'N/A' }}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-gray-900">{{ reg.member.phone || 'N/A' }}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span
                                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                                    {{ reg.category.name }}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                                {{ reg.total_to_pay }} €
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span v-if="parseFloat(reg.remaining_to_pay) > 0"
                                    class="text-sm font-bold text-red-600">
                                    {{ reg.remaining_to_pay }} €
                                </span>
                                <span v-else
                                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                    Réglé
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="text-sm text-gray-900">{{ reg.status }}</span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                <button @click="openPriceModal(reg)" class="text-judo-blue hover:text-blue-900">
                                    Modifier Tarif
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </BaseCard>

        <EditPriceModal :is-open="showPriceModal" :registration="editingRegistration" @close="showPriceModal = false"
            @saved="onRefresh" />

        <CreateRegistrationModal :is-open="showCreateModal" @close="showCreateModal = false" @created="onRefresh" />
    </div>
</template>

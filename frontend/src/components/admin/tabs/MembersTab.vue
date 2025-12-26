<script setup>
import { ref } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import MembersTable from '@/components/admin/MembersTable.vue'
import EditMemberModal from '@/components/admin/modals/EditMemberModal.vue'
import WeighInModal from '@/components/admin/modals/WeighInModal.vue'
import CreateUserModal from '@/components/admin/modals/CreateUserModal.vue'
import CreateMemberModal from '@/components/admin/modals/CreateMemberModal.vue'
import BulkEmailModal from '@/components/admin/modals/BulkEmailModal.vue'
import { Plus } from 'lucide-vue-next'

const props = defineProps({
    allMembers: {
        type: Array,
        default: () => []
    },
    registrations: {
        type: Array,
        default: () => []
    },
    categories: {
        type: Array,
        default: () => []
    },
    loadingMembers: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['refresh', 'export'])

// Modals State
const showEditMemberModal = ref(false)
const editingMember = ref(null)

const showMemberModal = ref(false)
const showWeighInModal = ref(false)
const weighInMember = ref(null)

const showUserModal = ref(false)

const showEmailModal = ref(false)
const selectedMembersForEmail = ref([])
const emailForm = ref({ subject: '', body: '' })

// Handlers
const openEditMemberModal = (member) => {
    editingMember.value = member
    showEditMemberModal.value = true
}

const openWeighInModal = (member) => {
    weighInMember.value = member
    showWeighInModal.value = true
}

const handleBulkEmailAction = (memberIds) => {
    selectedMembersForEmail.value = memberIds
    emailForm.value = { subject: '', body: '' }
    showEmailModal.value = true
}

const onRefresh = () => {
    emit('refresh')
}
</script>

<template>
    <div>
        <div class="flex justify-between items-center mb-6">
            <div>
                <h2 class="text-2xl font-bold text-gray-900">Gestion des Membres</h2>
                <p class="text-gray-500">{{ allMembers.length }} membres au total</p>
            </div>
            <div class="flex space-x-3">
                <BaseButton variant="primary" @click="showMemberModal = true">
                    <template #icon>
                        <Plus :size="20" />
                    </template>
                    Ajouter Membre
                </BaseButton>
                <BaseButton variant="white" @click="showUserModal = true">
                    <template #icon>
                        <Plus :size="20" />
                    </template>
                    Compte Parent
                </BaseButton>
            </div>
        </div>

        <MembersTable :members="allMembers" :registrations="registrations" :categories="categories"
            :loading="loadingMembers" @edit-member="openEditMemberModal" @weigh-in="openWeighInModal"
            @send-email="handleBulkEmailAction" @export-excel="$emit('export')" />

        <!-- Modals -->
        <EditMemberModal :is-open="showEditMemberModal" :member="editingMember" @close="showEditMemberModal = false"
            @saved="onRefresh" />

        <CreateMemberModal :is-open="showMemberModal" @close="showMemberModal = false" @created="onRefresh" />

        <WeighInModal :is-open="showWeighInModal" :member="weighInMember" @close="showWeighInModal = false"
            @saved="onRefresh" />

        <CreateUserModal :is-open="showUserModal" @close="showUserModal = false" @created="onRefresh" />

        <BulkEmailModal :is-open="showEmailModal" :selected-members="selectedMembersForEmail" :all-members="allMembers"
            :initial-subject="emailForm.subject" :initial-body="emailForm.body" @close="showEmailModal = false"
            @sent="onRefresh" />
    </div>
</template>

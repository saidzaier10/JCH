<script setup>
import { ref, computed, watch } from 'vue'
import {
    Users,
    Edit,
    Trash2,
    Search,
    Filter,
    Download,
    CheckCircle,
    XCircle,
    AlertCircle,
    Scale,
    ChevronLeft,
    ChevronRight,
    Mail
} from 'lucide-vue-next'
import BaseCard from '../ui/BaseCard.vue'
import BaseButton from '../ui/BaseButton.vue'
import BaseInput from '../ui/BaseInput.vue'
import BaseSelect from '../ui/BaseSelect.vue'

const props = defineProps({
    members: {
        type: Array,
        required: true
    },
    registrations: {
        type: Array,
        required: true
    },
    categories: {
        type: Array,
        default: () => []
    },
    loading: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['edit-member', 'weigh-in', 'send-email', 'export-excel'])

const memberSearch = ref('')
const filterCategory = ref('')
const filterStatus = ref('')
const selectedMembers = ref([])

// Helper function to check member status
const isMemberActive = (memberId) => {
    const reg = props.registrations.find(r => r.member.id === memberId)
    return reg && reg.paid
}

const getMemberCategory = (memberId) => {
    const reg = props.registrations.find(r => r.member.id === memberId)
    return reg ? reg.category.name : 'N/A'
}

const filteredMembers = computed(() => {
    let filtered = props.members

    if (memberSearch.value) {
        const search = memberSearch.value.toLowerCase()
        filtered = filtered.filter(m =>
            m.first_name.toLowerCase().includes(search) ||
            m.last_name.toLowerCase().includes(search) ||
            (m.email && m.email.toLowerCase().includes(search)) ||
            (m.parent_name && m.parent_name.toLowerCase().includes(search))
        )
    }

    if (filterCategory.value) {
        filtered = filtered.filter(m => {
            const reg = props.registrations.find(r => r.member.id === m.id)
            return reg && reg.category.id === parseInt(filterCategory.value)
        })
    }

    if (filterStatus.value) {
        filtered = filtered.filter(m => {
            const isActive = isMemberActive(m.id)
            return filterStatus.value === 'active' ? isActive : !isActive
        })
    }

    return filtered
})

const areAllSelected = computed(() => {
    return filteredMembers.value.length > 0 && selectedMembers.value.length === filteredMembers.value.length
})

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

const totalPages = computed(() => Math.ceil(filteredMembers.value.length / itemsPerPage.value))

const paginatedMembers = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value
    const end = start + itemsPerPage.value
    return filteredMembers.value.slice(start, end)
})

const nextPage = () => {
    if (currentPage.value < totalPages.value) currentPage.value++
}

const prevPage = () => {
    if (currentPage.value > 1) currentPage.value--
}

// Reset page when filters change
watch([memberSearch, filterCategory, filterStatus], () => {
    currentPage.value = 1
})

const toggleSelectAll = () => {
    if (areAllSelected.value) {
        selectedMembers.value = []
    } else {
        selectedMembers.value = filteredMembers.value.map(m => m.id)
    }
}

const handleExport = () => {
    emit('export-excel', selectedMembers.value)
}

const handleBulkEmail = () => {
    emit('send-email', selectedMembers.value)
}

const emailFilteredMembers = () => {
    const filteredIds = filteredMembers.value.map(m => m.id)
    emit('send-email', filteredIds)
}

const currentCategoryName = computed(() => {
    if (!filterCategory.value) return ''
    const cat = props.categories.find(c => c.id === parseInt(filterCategory.value))
    return cat ? cat.name : ''
})

</script>

<template>
    <div class="space-y-6">
        <!-- Filters & Actions -->
        <div
            class="flex flex-col md:flex-row justify-between items-center gap-4 bg-white p-4 rounded-lg shadow-sm border border-gray-100">
            <div class="relative w-full md:w-96">
                <BaseInput v-model="memberSearch" placeholder="Rechercher un adhérent..." id="member-search">
                    <template #prefix>
                        <Search :size="20" class="text-gray-400" />
                    </template>
                </BaseInput>
            </div>
            <div class="flex items-center space-x-3 w-full md:w-auto">
                <div class="relative w-48">
                    <BaseSelect v-model="filterCategory" id="filter-category">
                        <option value="">Toutes catégories</option>
                        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                            {{ cat.name }}
                        </option>
                    </BaseSelect>
                </div>
                <div class="relative w-48">
                    <BaseSelect v-model="filterStatus" id="filter-status">
                        <option value="">Tous les statuts</option>
                        <option value="active">Actif</option>
                        <option value="inactive">Inactif</option>
                    </BaseSelect>
                    <div class="absolute left-3 top-1/2 transform -translate-y-1/2 pointer-events-none"
                        v-if="!filterStatus">
                        <!-- Optional: Icon if needed, but BaseSelect doesn't support prefix slot yet easily without modification or wrapper. 
                             Actually BaseSelect doesn't have a prefix slot in my implementation. 
                             The original code had a Filter icon. 
                             I should probably just drop the icon or update BaseSelect to support it.
                             For now, I'll drop the icon to keep it simple as BaseSelect doesn't support it. -->
                    </div>
                </div>
                <!-- Email Filtered Button (Only if NO manual selection) -->
                <BaseButton v-if="filterCategory && filteredMembers.length > 0 && selectedMembers.length === 0"
                    variant="secondary" @click="emailFilteredMembers">
                    <template #icon>
                        <Mail :size="18" />
                    </template>
                    Email {{ currentCategoryName }} ({{ filteredMembers.length }})
                </BaseButton>

                <!-- Email Selected Button (Takes precedence) -->
                <BaseButton v-if="selectedMembers.length > 0" variant="primary" @click="handleBulkEmail">
                    <template #icon>
                        <Mail :size="18" />
                    </template>
                    Email ({{ selectedMembers.length }})
                </BaseButton>
                <BaseButton variant="white" @click="handleExport">
                    <template #icon>
                        <Download :size="18" />
                    </template>
                    Export
                </BaseButton>
            </div>
        </div>

        <!-- Members Table -->
        <BaseCard class="overflow-hidden">
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-4">
                                <input type="checkbox" :checked="areAllSelected" @change="toggleSelectAll"
                                    class="rounded border-gray-300 text-judo-blue focus:ring-judo-blue" />
                            </th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Adhérent
                            </th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Catégorie
                            </th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Statut
                            </th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Poids
                            </th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-if="loading" class="animate-pulse">
                            <td colspan="6" class="px-6 py-4 text-center text-gray-500">Chargement...</td>
                        </tr>
                        <tr v-else-if="filteredMembers.length === 0">
                            <td colspan="6" class="px-6 py-12 text-center text-gray-500">
                                <Users :size="48" class="mx-auto mb-3 text-gray-300" />
                                <p>Aucun membre trouvé</p>
                            </td>
                        </tr>
                        <tr v-else v-for="member in paginatedMembers" :key="member.id"
                            class="hover:bg-gray-50 transition duration-150">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <input type="checkbox" v-model="selectedMembers" :value="member.id"
                                    class="rounded border-gray-300 text-judo-blue focus:ring-judo-blue" />
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <div
                                        class="w-10 h-10 rounded-full bg-judo-blue/10 flex items-center justify-center shrink-0">
                                        <Users :size="20" class="text-judo-blue" />
                                    </div>
                                    <div class="ml-4">
                                        <div class="text-sm font-medium text-gray-900">
                                            {{ member.first_name }} {{ member.last_name }}
                                        </div>
                                        <div class="text-sm text-gray-500">{{ member.email }}</div>
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span
                                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                                    {{ getMemberCategory(member.id) }}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span v-if="isMemberActive(member.id)"
                                    class="flex items-center text-green-600 text-sm font-medium">
                                    <CheckCircle :size="16" class="mr-1" /> Actif
                                </span>
                                <span v-else class="flex items-center text-gray-500 text-sm">
                                    <AlertCircle :size="16" class="mr-1" /> En attente
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <span v-if="member.weight_category" class="text-gray-900 font-bold">
                                    {{ member.weight_category }} kg
                                </span>
                                <span v-else class="text-gray-400 italic text-xs">Non pesé</span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <div class="flex items-center space-x-3">
                                    <button @click="$emit('weigh-in', member)"
                                        class="flex items-center text-orange-600 hover:text-orange-900 bg-orange-50 hover:bg-orange-100 px-3 py-1.5 rounded-md transition-colors"
                                        title="Pesée">
                                        <Scale :size="16" class="mr-1.5" />
                                        <span>Peser</span>
                                    </button>
                                    <button @click="$emit('edit-member', member)"
                                        class="flex items-center text-blue-600 hover:text-blue-900 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-md transition-colors">
                                        <Edit :size="16" class="mr-1.5" />
                                        <span>Modifier</span>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Pagination Controls -->
            <div class="bg-gray-50 px-4 py-3 border-t border-gray-200 flex items-center justify-between sm:px-6">
                <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                    <div>
                        <p class="text-sm text-gray-700">
                            Affichage de <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span> à
                            <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, filteredMembers.length)
                                }}</span>
                            sur <span class="font-medium">{{ filteredMembers.length }}</span> résultats
                        </p>
                    </div>
                    <div>
                        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                            <button @click="prevPage" :disabled="currentPage === 1"
                                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                                <span class="sr-only">Précédent</span>
                                <ChevronLeft :size="20" />
                            </button>
                            <button @click="nextPage" :disabled="currentPage === totalPages"
                                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                                <span class="sr-only">Suivant</span>
                                <ChevronRight :size="20" />
                            </button>
                        </nav>
                    </div>
                </div>
            </div>
        </BaseCard>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import CreateUserModal from '@/components/admin/modals/CreateUserModal.vue'
import EditUserModal from '@/components/admin/modals/EditUserModal.vue'
import api from '@/utils/axios'
import { Users, Search } from 'lucide-vue-next'
import { useToastStore } from '@/stores/toast'

const showUserModal = ref(false)
const showEditUserModal = ref(false)
const editingUser = ref(null)
const users = ref([])
const loading = ref(false)
const search = ref('')
const toast = useToastStore()

const openEditModal = (user) => {
    editingUser.value = user
    showEditUserModal.value = true
}

const fetchUsers = async () => {
    loading.value = true
    try {
        const params = {}
        if (search.value) params.search = search.value

        const res = await api.get('/api/users/', { params })
        users.value = res.data.results || res.data
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors du chargement des utilisateurs")
    } finally {
        loading.value = false
    }
}

let timeout = null
watch(search, () => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
        fetchUsers()
    }, 300)
})

onMounted(() => {
    fetchUsers()
})
</script>

<template>
    <div class="space-y-6">
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Gestion des Utilisateurs</h2>
            <BaseButton variant="primary" @click="showUserModal = true">
                <template #icon>👤</template>
                Créer un compte Parent
            </BaseButton>
        </div>

        <!-- Filters -->
        <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100 mb-6">
            <div class="relative max-w-md">
                <BaseInput v-model="search" placeholder="Rechercher (nom, email...)" id="user-search">
                    <template #prefix>
                        <Search :size="20" class="text-gray-400" />
                    </template>
                </BaseInput>
            </div>
        </div>

        <BaseCard class="overflow-hidden">
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Utilisateur</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Email</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Rôle</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Date d'inscription</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Actions</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-if="loading" class="animate-pulse">
                            <td colspan="5" class="px-6 py-4 text-center text-gray-500">Chargement...</td>
                        </tr>
                        <tr v-else-if="users.length === 0">
                            <td colspan="5" class="px-6 py-12 text-center text-gray-500">
                                <Users :size="48" class="mx-auto mb-3 text-gray-300" />
                                <p>Aucun utilisateur trouvé</p>
                            </td>
                        </tr>
                        <tr v-else v-for="user in users" :key="user.id" class="hover:bg-gray-50 transition">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <div
                                        class="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold mr-3">
                                        {{ user.username.charAt(0).toUpperCase() }}
                                    </div>
                                    <div class="text-sm font-medium text-gray-900">{{ user.username }}</div>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.email }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span v-if="user.is_staff"
                                    class="px-2 py-1 text-xs font-semibold rounded-full bg-purple-100 text-purple-800">Admin</span>
                                <span v-else
                                    class="px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800">Parent</span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {{ new Date(user.date_joined).toLocaleDateString() }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <button @click="openEditModal(user)" class="text-indigo-600 hover:text-indigo-900">
                                    Modifier
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </BaseCard>

        <CreateUserModal :is-open="showUserModal" @close="showUserModal = false" @created="fetchUsers" />
        <EditUserModal :is-open="showEditUserModal" :user="editingUser" @close="showEditUserModal = false"
            @updated="fetchUsers" />
    </div>
</template>

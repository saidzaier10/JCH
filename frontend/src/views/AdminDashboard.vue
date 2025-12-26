<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/utils/axios'
import { useToastStore } from '@/stores/toast'
import {
    LayoutDashboard,
    Users,
    ClipboardList,
    Wallet,
    Calendar,
    ClipboardCheck,
    Settings,
    UserCog,
    LogOut,
    ImageIcon,
    ExternalLink
} from 'lucide-vue-next'

// Components
import DashboardStats from '@/components/admin/DashboardStats.vue'
import EventList from '@/components/EventList.vue'
import ConvocationManager from '@/components/ConvocationManager.vue'
import AttendanceSheet from '@/components/admin/AttendanceSheet.vue'
import CourseManager from '@/components/admin/CourseManager.vue'
import SeasonManager from '@/components/admin/SeasonManager.vue'
import GalleryManager from '@/components/admin/GalleryManager.vue'

// New Tab Components
import MembersTab from '@/components/admin/tabs/MembersTab.vue'
import RegistrationsTab from '@/components/admin/tabs/RegistrationsTab.vue'
import FinancesTab from '@/components/admin/tabs/FinancesTab.vue'
import UsersTab from '@/components/admin/tabs/UsersTab.vue'

const router = useRouter()
const toast = useToastStore()

// State
const currentTab = ref('dashboard')
const attendanceSubTab = ref('sheets')
const loading = ref(true)
const loadingMembers = ref(false)
const loadingRegistrations = ref(false)

// Data
const stats = ref(null)
const registrations = ref([])
const allMembers = ref([])
const categories = ref([])
const events = ref([])

// Events State
const selectedEvent = ref(null)

// Computed
const financialStats = computed(() => {
    // Calcul des statistiques financières (Chiffre d'affaires payé vs en attente)
    const paid = registrations.value.filter(r => r.paid)
    const pending = registrations.value.filter(r => !r.paid)

    return {
        paid_revenue: paid.reduce((sum, r) => sum + parseFloat(r.category.price), 0),
        paid_count: paid.length,
        pending_revenue: pending.reduce((sum, r) => sum + parseFloat(r.category.price), 0),
        pending_count: pending.length
    }
})

const paymentRate = computed(() => {
    if (registrations.value.length === 0) return 0
    const paid = registrations.value.filter(r => r.paid).length
    return Math.round((paid / registrations.value.length) * 100)
})

// Actions
const fetchStats = async () => {
    try {
        const res = await api.get('/api/registrations/stats/')
        stats.value = res.data
    } catch (e) {
        console.error(e)
    }
}

const fetchRegistrations = async () => {
    loadingRegistrations.value = true
    try {
        const res = await api.get('/api/registrations/?all=true')
        registrations.value = res.data.results || res.data
    } catch (e) {
        console.error(e)
        // toast.error("Erreur chargement inscriptions")
    } finally {
        loadingRegistrations.value = false
    }
}

const fetchMembers = async () => {
    loadingMembers.value = true
    try {
        const res = await api.get('/api/members/?all=true')
        allMembers.value = res.data.results || res.data
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors du chargement des membres")
    } finally {
        loadingMembers.value = false
    }
}

const fetchCategories = async () => {
    try {
        const res = await api.get('/api/categories/')
        categories.value = res.data.results || res.data
    } catch (e) {
        console.error(e)
    }
}

const fetchEvents = async () => {
    try {
        const res = await api.get('/api/events/')
        events.value = res.data.results || res.data
    } catch (e) {
        console.error(e)
    }
}

const exportExcel = async () => {
    try {
        const response = await api.get('/api/registrations/export/', {
            responseType: 'blob', // Important for file download
        })

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `inscriptions_${new Date().toISOString().slice(0, 10)}.xlsx`)
        document.body.appendChild(link)
        link.click()
        link.remove()
    } catch (e) {
        console.error("Erreur export excel", e)
        alert("Erreur lors de l'export")
    }
}

const selectEvent = (event) => {
    selectedEvent.value = event
}

const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('username')
    localStorage.removeItem('is_staff')
    router.push('/login')
}

// Watchers
// Watchers pour charger les données uniquement quand l'onglet est actif
watch(currentTab, (newTab) => {
    if (newTab === 'registrations' && registrations.value.length === 0) {
        fetchRegistrations()
    }
    if (newTab === 'members' && allMembers.value.length === 0) {
        fetchMembers()
    }
    if (newTab === 'finances') {
        fetchRegistrations()
        fetchStats()
    }
})

// Init
onMounted(async () => {
    // Chargement initial des données critiques
    await Promise.all([
        fetchStats(),
        fetchCategories(),
        fetchEvents()
    ])
    // Pré-chargement des données lourdes en arrière-plan
    fetchRegistrations()
    fetchMembers()
    loading.value = false
})
</script>

<template>
    <div class="flex h-screen bg-gray-100 font-sans">
        <!-- Sidebar -->
        <div class="w-64 bg-judo-blue text-white flex flex-col shadow-2xl relative overflow-hidden">
            <div class="absolute inset-0 bg-linear-to-b from-blue-900/50 to-transparent pointer-events-none"></div>
            <div class="p-6 border-b border-blue-800/50">
                <div class="flex items-center space-x-2">
                    <div class="w-10 h-10 bg-white/10 rounded-lg flex items-center justify-center">
                        <span class="text-2xl">🥋</span>
                    </div>
                    <div>
                        <h1 class="text-xl font-bold tracking-wide">Judo Club Hem</h1>
                        <p class="text-xs text-blue-200">Administration</p>
                    </div>
                </div>
            </div>
            <nav class="flex-1 p-4 space-y-1">
                <a href="#" @click.prevent="currentTab = 'dashboard'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'dashboard' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <LayoutDashboard :size="20" class="mr-3" />
                    <span>Vue d'ensemble</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'members'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'members' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <Users :size="20" class="mr-3" />
                    <span>Membres</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'registrations'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'registrations' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <ClipboardList :size="20" class="mr-3" />
                    <span>Inscriptions</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'finances'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'finances' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <Wallet :size="20" class="mr-3" />
                    <span>Finances</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'events'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'events' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <Calendar :size="20" class="mr-3" />
                    <span>Événements</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'attendance'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'attendance' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <ClipboardCheck :size="20" class="mr-3" />
                    <span>Présences</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'seasons'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'seasons' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <Settings :size="20" class="mr-3" />
                    <span>Saisons & Catégories</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'gallery'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'gallery' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <ImageIcon :size="20" class="mr-3" />
                    <span>Galerie</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'users'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'users' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <UserCog :size="20" class="mr-3" />
                    <span>Utilisateurs</span>
                </a>

                <div class="pt-4 mt-4 border-t border-blue-800/50">
                    <a href="https://moncompte.ffjudo.com" target="_blank" rel="noopener noreferrer"
                        class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group text-blue-100 hover:bg-white/10 hover:text-white">
                        <ExternalLink :size="20" class="mr-3" />
                        <span>Compte FFJudo</span>
                    </a>
                    <a href="https://www.comitenordjudo.fr" target="_blank" rel="noopener noreferrer"
                        class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group text-blue-100 hover:bg-white/10 hover:text-white">
                        <ExternalLink :size="20" class="mr-3" />
                        <span>Comité Nord Judo</span>
                    </a>
                    <a href="https://hautsdefrancejudo.ffjudo.com" target="_blank" rel="noopener noreferrer"
                        class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group text-blue-100 hover:bg-white/10 hover:text-white">
                        <ExternalLink :size="20" class="mr-3" />
                        <span>Ligue HDF Judo</span>
                    </a>
                </div>
            </nav>
            <div class="p-4 border-t border-blue-800/50">
                <button @click="logout"
                    class="w-full flex items-center justify-center px-4 py-2 text-sm text-blue-200 hover:text-white hover:bg-white/10 rounded-lg transition">
                    <LogOut :size="18" class="mr-2" />
                    Déconnexion
                </button>
            </div>
        </div>

        <!-- Content -->
        <div class="flex-1 overflow-auto">
            <div class="p-8 max-w-7xl mx-auto">
                <!-- Dashboard Tab -->
                <div v-if="currentTab === 'dashboard'">
                    <DashboardStats :stats="stats" :registrations="registrations" :events="events" :loading="loading" />
                </div>

                <!-- Members Tab -->
                <div v-if="currentTab === 'members'">
                    <MembersTab :all-members="allMembers" :registrations="registrations" :categories="categories"
                        :loading-members="loadingMembers" @refresh="fetchMembers" @export="exportExcel" />
                </div>

                <!-- Finances Tab -->
                <div v-if="currentTab === 'finances'">
                    <FinancesTab :registrations="registrations" :financial-stats="financialStats" :stats="stats"
                        :payment-rate="paymentRate" :loading="loadingRegistrations" :all-members="allMembers"
                        @refresh="fetchRegistrations(); fetchStats()" />
                </div>

                <!-- Registrations Tab -->
                <div v-if="currentTab === 'registrations'">
                    <RegistrationsTab :registrations="registrations" :loading="loadingRegistrations"
                        @refresh="fetchRegistrations(); fetchStats()" @export="exportExcel" />
                </div>

                <!-- Events Tab -->
                <div v-if="currentTab === 'events'">
                    <EventList v-if="!selectedEvent" @manage-convocations="selectEvent" />
                    <ConvocationManager v-else :event="selectedEvent" @back="selectedEvent = null" />
                </div>

                <!-- Attendance Tab -->
                <div v-if="currentTab === 'attendance'">
                    <div class="mb-6 flex space-x-4">
                        <button @click="attendanceSubTab = 'sheets'"
                            class="px-4 py-2 rounded-lg font-medium transition-colors"
                            :class="attendanceSubTab === 'sheets' ? 'bg-judo-blue text-white' : 'bg-white text-gray-600 hover:bg-gray-50'">
                            Feuilles de présence
                        </button>
                        <button @click="attendanceSubTab = 'courses'"
                            class="px-4 py-2 rounded-lg font-medium transition-colors"
                            :class="attendanceSubTab === 'courses' ? 'bg-judo-blue text-white' : 'bg-white text-gray-600 hover:bg-gray-50'">
                            Gestion des Cours
                        </button>
                    </div>

                    <AttendanceSheet v-if="attendanceSubTab === 'sheets'" />
                    <CourseManager v-else />
                </div>

                <!-- Seasons & Categories Tab -->
                <div v-if="currentTab === 'seasons'">
                    <SeasonManager />
                </div>

                <!-- Gallery Tab -->
                <div v-if="currentTab === 'gallery'">
                    <GalleryManager />
                </div>

                <!-- Users Tab -->
                <div v-if="currentTab === 'users'">
                    <UsersTab />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
    ArcElement
} from 'chart.js'
import { Bar, Pie } from 'vue-chartjs'
import {
    Users,
    Calendar,
    TrendingUp,
    UserCog,
    Wallet,
    ClipboardCheck
} from 'lucide-vue-next'
import BaseCard from '../ui/BaseCard.vue'

// Register ChartJS components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement)

const props = defineProps({
    stats: {
        type: Object,
        default: null
    },
    registrations: {
        type: Array,
        default: () => []
    },
    events: {
        type: Array,
        default: () => []
    },
    loading: {
        type: Boolean,
        default: false
    }
})

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false
}

// Computed Data
const upcomingEventsCount = computed(() => {
    if (!props.events || props.events.length === 0) return 0
    const now = new Date()
    // Calculate events starting in the future
    return props.events.filter(e => new Date(e.start_time) > now).length
})

const actionItems = computed(() => {
    const items = []

    // Unpaid registrations
    const unpaidCount = props.registrations.filter(r => !r.paid).length
    if (unpaidCount > 0) {
        items.push({
            label: 'Paiements en attente',
            count: unpaidCount,
            color: 'text-orange-600',
            bg: 'bg-orange-100',
            icon: Wallet
        })
    }

    return items
})

const paymentRate = computed(() => {
    if (props.registrations.length === 0) return 0
    const paidCount = props.registrations.filter(r => r.paid).length
    return Math.round((paidCount / props.registrations.length) * 100)
})

const barChartData = computed(() => {
    if (!props.stats) return null

    const labels = props.stats?.registrations_per_category?.map(item => item.category__name) || []
    const data = props.stats?.registrations_per_category?.map(item => item.count) || []

    return {
        labels,
        datasets: [{
            label: 'Inscrits',
            backgroundColor: '#f87171',
            data
        }]
    }
})

const pieChartData = computed(() => {
    if (!props.stats) return null

    const labels = props.stats?.gender_distribution?.map(item => item.gender === 'M' ? 'Masculin' : 'Féminin') || []
    const data = props.stats?.gender_distribution?.map(item => item.count) || []

    return {
        labels,
        datasets: [{
            backgroundColor: ['#3b82f6', '#ec4899'],
            data
        }]
    }
})

const recentActivities = computed(() => {
    const activities = []

    // Add registration activities
    const recentRegs = props.registrations.slice(0, 5)
    recentRegs.forEach(reg => {
        activities.push({
            icon: UserCog,
            iconBg: 'bg-blue-100',
            iconColor: 'text-blue-600',
            title: `Nouvelle inscription: ${reg.member.first_name} ${reg.member.last_name}`,
            time: 'Il y a 2 heures'
        })
    })

    // Add payment activities
    const paidRegs = props.registrations.filter(r => r.paid).slice(0, 3)
    paidRegs.forEach(reg => {
        activities.push({
            icon: Wallet,
            iconBg: 'bg-green-100',
            iconColor: 'text-green-600',
            title: `Paiement reçu: ${reg.member.first_name} ${reg.member.last_name}`,
            time: 'Il y a 5 heures'
        })
    })

    return activities.slice(0, 10)
})
</script>

<template>
    <div>
        <div class="mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Tableau de Bord</h2>
            <p class="text-gray-500">Aperçu général de l'activité du club</p>
        </div>

        <div v-if="loading" class="flex justify-center py-20">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-judo-blue"></div>
        </div>

        <div v-else>
            <!-- KPI Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <BaseCard class="border-l-4 border-l-blue-500 hover:shadow-lg transition-shadow">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="text-gray-500 text-sm font-medium uppercase tracking-wider">Total Membres
                            </h3>
                            <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats?.total_members || 0 }}</p>
                            <div class="flex items-center mt-2">
                                <Users :size="16" class="text-green-500 mr-1" />
                                <span class="text-xs text-green-600 font-medium">+12% vs dernier mois</span>
                            </div>
                        </div>
                        <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                            <Users :size="24" class="text-blue-600" />
                        </div>
                    </div>
                </BaseCard>

                <BaseCard class="border-l-4 border-l-purple-500 hover:shadow-lg transition-shadow">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="text-gray-500 text-sm font-medium uppercase tracking-wider">
                                Événements</h3>
                            <p class="text-3xl font-bold text-gray-900 mt-2">{{ upcomingEventsCount }}</p>
                            <div class="flex items-center mt-2">
                                <Calendar :size="16" class="text-purple-500 mr-1" />
                                <span class="text-xs text-purple-600 font-medium">à venir</span>
                            </div>
                        </div>
                        <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                            <Calendar :size="24" class="text-purple-600" />
                        </div>
                    </div>
                </BaseCard>

                <BaseCard class="border-l-4 border-l-orange-500 hover:shadow-lg transition-shadow">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="text-gray-500 text-sm font-medium uppercase tracking-wider">Taux
                                Paiement</h3>
                            <p class="text-3xl font-bold text-gray-900 mt-2">{{ paymentRate }}%</p>
                            <div class="flex items-center mt-2">
                                <TrendingUp :size="16" class="text-green-500 mr-1" />
                                <span class="text-xs text-green-600 font-medium">+5% vs dernier mois</span>
                            </div>
                        </div>
                        <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                            <TrendingUp :size="24" class="text-orange-600" />
                        </div>
                    </div>
                </BaseCard>

                <!-- Actions Required Card -->
                <BaseCard class="border-l-4 border-l-red-500 hover:shadow-lg transition-shadow">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="text-gray-500 text-sm font-medium uppercase tracking-wider">À Traiter
                            </h3>
                            <p class="text-3xl font-bold text-gray-900 mt-2">{{ actionItems.length }}</p>
                            <div class="flex flex-col mt-2 gap-1">
                                <span v-for="item in actionItems" :key="item.label" class="text-xs font-medium"
                                    :class="item.color">
                                    {{ item.count }} {{ item.label }}
                                </span>
                                <span v-if="actionItems.length === 0" class="text-xs text-green-600 font-medium">
                                    Tout est à jour !
                                </span>
                            </div>
                        </div>
                        <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                            <ClipboardCheck :size="24" class="text-red-600" />
                        </div>
                    </div>
                </BaseCard>
            </div>

            <!-- Charts and Activity Feed -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Charts (2 columns) -->
                <div class="lg:col-span-2 space-y-6">
                    <BaseCard>
                        <template #header>
                            <h3 class="text-lg font-bold text-gray-900">Inscriptions par Catégorie</h3>
                        </template>
                        <div class="h-64">
                            <Bar v-if="barChartData" :data="barChartData" :options="chartOptions" />
                        </div>
                    </BaseCard>

                    <BaseCard>
                        <template #header>
                            <h3 class="text-lg font-bold text-gray-900">Répartition Hommes/Femmes</h3>
                        </template>
                        <div class="h-64 flex justify-center">
                            <Pie v-if="pieChartData" :data="pieChartData" :options="chartOptions" />
                        </div>
                    </BaseCard>
                </div>

                <!-- Activity Feed (1 column) -->
                <div>
                    <BaseCard class="h-full">
                        <template #header>
                            <h3 class="text-lg font-bold text-gray-900">Activité Récente</h3>
                        </template>
                        <div class="space-y-4 max-h-[600px] overflow-y-auto">
                            <div v-for="(activity, index) in recentActivities" :key="index"
                                class="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition">
                                <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0"
                                    :class="activity.iconBg">
                                    <component :is="activity.icon" :size="16" :class="activity.iconColor" />
                                </div>
                                <div class="flex-1 min-w-0">
                                    <p class="text-sm text-gray-900">{{ activity.title }}</p>
                                    <p class="text-xs text-gray-500 mt-1">{{ activity.time }}</p>
                                </div>
                            </div>
                        </div>
                    </BaseCard>
                </div>
            </div>
        </div>
    </div>
</template>

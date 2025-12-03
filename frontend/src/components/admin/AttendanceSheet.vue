<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { Calendar, Save, CheckCircle, XCircle, AlertCircle } from 'lucide-vue-next'
import api from '@/utils/axios'
import BaseButton from '../ui/BaseButton.vue'
import BaseInput from '../ui/BaseInput.vue'
import BaseSelect from '../ui/BaseSelect.vue'
import BaseCard from '../ui/BaseCard.vue'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()
const courses = ref([])
const members = ref([])
const categories = ref([])
const session = ref(null)
const loading = ref(false)
const saving = ref(false)

const selectedCourseId = ref('')
const selectedDate = ref(new Date().toISOString().slice(0, 10))
const selectedCategory = ref('')

// Attendance state: Map of memberId -> status
const attendanceMap = ref({})

const fetchInitialData = async () => {
    try {
        const [coursesRes, membersRes, categoriesRes] = await Promise.all([
            api.get('/api/courses/'),
            api.get('/api/members/'),
            api.get('/api/categories/')
        ])
        courses.value = coursesRes.data
        members.value = membersRes.data
        categories.value = categoriesRes.data
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors du chargement des données")
    }
}

const fetchSession = async () => {
    if (!selectedCourseId.value || !selectedDate.value) return

    loading.value = true
    try {
        const res = await api.get('/api/sessions/get_by_date_and_course/', {
            params: {
                date: selectedDate.value,
                course_id: selectedCourseId.value
            }
        })
        session.value = res.data

        // Initialize attendance map from session data
        attendanceMap.value = {}
        if (session.value.attendances) {
            session.value.attendances.forEach(a => {
                attendanceMap.value[a.member] = a.status
            })
        }
    } catch (e) {
        console.error(e)
        // Session might not exist yet, that's fine
        session.value = null
        attendanceMap.value = {}
    } finally {
        loading.value = false
    }
}

const filteredMembers = computed(() => {
    let result = members.value

    // Filter by category if selected
    if (selectedCategory.value) {
        const cat = categories.value.find(c => c.id === selectedCategory.value)
        if (cat) {
            result = result.filter(m => {
                if (!m.birth_date) return false
                const age = new Date().getFullYear() - new Date(m.birth_date).getFullYear()
                return age >= cat.age_min && age <= cat.age_max
            })
        }
    }

    // Sort by name
    return result.sort((a, b) => a.last_name.localeCompare(b.last_name))
})

const getStatus = (memberId) => {
    return attendanceMap.value[memberId] || 'ABSENT' // Default to absent if not set? Or maybe null
}

const setStatus = (memberId, status) => {
    attendanceMap.value[memberId] = status
}

const saveAttendance = async () => {
    if (!selectedCourseId.value || !selectedDate.value) return

    saving.value = true
    try {
        // First ensure session exists
        if (!session.value) {
            const sessionRes = await api.post('/api/sessions/', {
                course: selectedCourseId.value,
                date: selectedDate.value
            })
            session.value = sessionRes.data
        }

        // Prepare attendance data
        const attendances = Object.entries(attendanceMap.value).map(([memberId, status]) => ({
            member_id: parseInt(memberId),
            status
        }))

        await api.post(`/api/sessions/${session.value.id}/mark_attendance/`, {
            attendances
        })

        toast.success("Présences enregistrées")
        fetchSession() // Refresh
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de l'enregistrement")
    } finally {
        saving.value = false
    }
}

const markAllPresent = () => {
    filteredMembers.value.forEach(m => {
        attendanceMap.value[m.id] = 'PRESENT'
    })
}

watch([selectedCourseId, selectedDate], fetchSession)
onMounted(fetchInitialData)
</script>

<template>
    <BaseCard class="p-6">
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-bold text-gray-800">Feuille de Présence</h2>
            <BaseButton variant="primary" @click="saveAttendance" :disabled="saving || !selectedCourseId">
                <template #icon>
                    <Save :size="20" />
                </template>
                {{ saving ? 'Enregistrement...' : 'Enregistrer' }}
            </BaseButton>
        </div>

        <!-- Filters -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 bg-gray-50 p-4 rounded-lg">
            <BaseInput type="date" v-model="selectedDate" label="Date" />
            <div>
                <BaseSelect id="course-select" label="Cours" v-model="selectedCourseId">
                    <option value="" disabled>Sélectionner un cours</option>
                    <option v-for="course in courses" :key="course.id" :value="course.id">
                        {{ course.name }} ({{ course.day_of_week_display }})
                    </option>
                </BaseSelect>
            </div>
            <div>
                <BaseSelect id="category-select" label="Filtrer par catégorie (Optionnel)" v-model="selectedCategory">
                    <option value="">Tous les membres</option>
                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                        {{ cat.name }}
                    </option>
                </BaseSelect>
            </div>
        </div>

        <div v-if="!selectedCourseId" class="text-center py-12 text-gray-500">
            <Calendar :size="48" class="mx-auto mb-4 text-gray-300" />
            <p>Veuillez sélectionner un cours et une date pour commencer.</p>
        </div>

        <div v-else>
            <div class="flex justify-between items-center mb-4">
                <p class="text-sm text-gray-600">{{ filteredMembers.length }} membres affichés</p>
                <button @click="markAllPresent" class="text-sm text-blue-600 hover:text-blue-800 font-medium">
                    Tout marquer comme présent
                </button>
            </div>

            <div class="overflow-x-auto border rounded-lg max-h-[600px] overflow-y-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50 sticky top-0 z-10">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Membre
                            </th>
                            <th
                                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Présent
                            </th>
                            <th
                                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Absent
                            </th>
                            <th
                                class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Excusé
                            </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="member in filteredMembers" :key="member.id" class="hover:bg-gray-50">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm font-medium text-gray-900">
                                    {{ member.last_name }} {{ member.first_name }}
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-center">
                                <button @click="setStatus(member.id, 'PRESENT')"
                                    class="p-2 rounded-full transition-colors"
                                    :class="getStatus(member.id) === 'PRESENT' ? 'bg-green-100 text-green-600' : 'text-gray-300 hover:bg-gray-100'">
                                    <CheckCircle :size="24" />
                                </button>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-center">
                                <button @click="setStatus(member.id, 'ABSENT')"
                                    class="p-2 rounded-full transition-colors"
                                    :class="getStatus(member.id) === 'ABSENT' ? 'bg-red-100 text-red-600' : 'text-gray-300 hover:bg-gray-100'">
                                    <XCircle :size="24" />
                                </button>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-center">
                                <button @click="setStatus(member.id, 'EXCUSED')"
                                    class="p-2 rounded-full transition-colors"
                                    :class="getStatus(member.id) === 'EXCUSED' ? 'bg-orange-100 text-orange-600' : 'text-gray-300 hover:bg-gray-100'">
                                    <AlertCircle :size="24" />
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </BaseCard>
</template>

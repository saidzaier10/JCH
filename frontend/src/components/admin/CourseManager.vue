<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Edit, Trash2, Clock, Calendar } from 'lucide-vue-next'
import api from '@/utils/axios'
import BaseButton from '../ui/BaseButton.vue'
import BaseInput from '../ui/BaseInput.vue'
import BaseSelect from '../ui/BaseSelect.vue'
import BaseTextarea from '../ui/BaseTextarea.vue'
import BaseCard from '../ui/BaseCard.vue'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()
const courses = ref([])
const loading = ref(false)
const showModal = ref(false)
const editingCourse = ref(null)

const form = ref({
    name: '',
    day_of_week: 0,
    start_time: '',
    end_time: '',
    teacher: '',
    description: ''
})

const daysOfWeek = [
    { value: 0, label: 'Lundi' },
    { value: 1, label: 'Mardi' },
    { value: 2, label: 'Mercredi' },
    { value: 3, label: 'Jeudi' },
    { value: 4, label: 'Vendredi' },
    { value: 5, label: 'Samedi' },
    { value: 6, label: 'Dimanche' }
]

const fetchCourses = async () => {
    loading.value = true
    try {
        const res = await api.get('/api/courses/')
        courses.value = res.data.results || res.data
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors du chargement des cours")
    } finally {
        loading.value = false
    }
}

const openModal = (course = null) => {
    if (course) {
        editingCourse.value = course
        form.value = { ...course }
    } else {
        editingCourse.value = null
        form.value = {
            name: '',
            day_of_week: 0,
            start_time: '',
            end_time: '',
            teacher: '',
            description: ''
        }
    }
    showModal.value = true
}

const saveCourse = async () => {
    try {
        if (editingCourse.value) {
            await api.patch(`/api/courses/${editingCourse.value.id}/`, form.value)
            toast.success("Cours modifié avec succès")
        } else {
            await api.post('/api/courses/', form.value)
            toast.success("Cours créé avec succès")
        }
        showModal.value = false
        fetchCourses()
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de l'enregistrement")
    }
}

const deleteCourse = async (id) => {
    if (!confirm("Êtes-vous sûr de vouloir supprimer ce cours ?")) return
    try {
        await api.delete(`/api/courses/${id}/`)
        toast.success("Cours supprimé")
        fetchCourses()
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de la suppression")
    }
}

const getDayLabel = (dayValue) => {
    const day = daysOfWeek.find(d => d.value === dayValue)
    return day ? day.label : 'Inconnu'
}

const formatTime = (timeString) => {
    if (!timeString) return ''
    return timeString.substring(0, 5)
}

onMounted(fetchCourses)
</script>

<template>
    <BaseCard class="p-6">
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-bold text-gray-800">Gestion des Cours</h2>
            <BaseButton variant="primary" @click="openModal()">
                <template #icon>
                    <Plus :size="20" />
                </template>
                Nouveau Cours
            </BaseButton>
        </div>

        <div v-if="loading" class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-judo-blue"></div>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="course in courses" :key="course.id"
                class="border rounded-lg p-4 hover:shadow-md transition-shadow bg-gray-50">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="font-bold text-lg text-gray-900">{{ course.name }}</h3>
                    <div class="flex space-x-2">
                        <button @click="openModal(course)" class="text-blue-600 hover:text-blue-800">
                            <Edit :size="18" />
                        </button>
                        <button @click="deleteCourse(course.id)" class="text-red-600 hover:text-red-800">
                            <Trash2 :size="18" />
                        </button>
                    </div>
                </div>

                <div class="space-y-2 text-sm text-gray-600">
                    <div class="flex items-center">
                        <Calendar :size="16" class="mr-2 text-gray-400" />
                        <span class="font-medium">{{ getDayLabel(course.day_of_week) }}</span>
                    </div>
                    <div class="flex items-center">
                        <Clock :size="16" class="mr-2 text-gray-400" />
                        <span>{{ formatTime(course.start_time) }} - {{ formatTime(course.end_time) }}</span>
                    </div>
                    <div v-if="course.teacher" class="flex items-center">
                        <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                            Prof: {{ course.teacher }}
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog"
            aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                    @click="showModal = false"></div>

                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

                <div
                    class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-100">
                    <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <h3 class="text-lg leading-6 font-bold text-gray-900 mb-4" id="modal-title">
                            {{ editingCourse ? `Modifier le cours : ${editingCourse.name}` : 'Nouveau cours' }}
                        </h3>
                        <form @submit.prevent="saveCourse" class="space-y-4">
                            <BaseInput v-model="form.name" label="Nom du cours" placeholder="Ex: Judo Enfant"
                                required />

                            <div>
                                <BaseSelect id="course-day" label="Jour" v-model="form.day_of_week">
                                    <option v-for="day in daysOfWeek" :key="day.value" :value="day.value">
                                        {{ day.label }}
                                    </option>
                                </BaseSelect>
                            </div>

                            <div class="grid grid-cols-2 gap-4">
                                <BaseInput type="time" v-model="form.start_time" label="Début" required />
                                <BaseInput type="time" v-model="form.end_time" label="Fin" required />
                            </div>

                            <BaseInput v-model="form.teacher" label="Professeur" placeholder="Nom du professeur" />

                            <div>
                                <BaseTextarea id="course-description" label="Description" v-model="form.description"
                                    rows="3" />
                            </div>

                            <div
                                class="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-3 space-y-3 space-y-reverse sm:space-y-0 mt-6">
                                <BaseButton type="button" variant="white" @click="showModal = false"
                                    class="w-full sm:w-auto">
                                    Annuler
                                </BaseButton>
                                <BaseButton type="submit" variant="primary" class="w-full sm:w-auto">
                                    Enregistrer
                                </BaseButton>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </BaseCard>
</template>

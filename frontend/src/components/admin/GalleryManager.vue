<script setup>
import { ref, onMounted, computed } from 'vue'
import { Trash2, Upload, Image as ImageIcon, CheckCircle } from 'lucide-vue-next'
import BaseCard from '../ui/BaseCard.vue'
import BaseButton from '../ui/BaseButton.vue'
import BaseInput from '../ui/BaseInput.vue'
import BaseSelect from '../ui/BaseSelect.vue'
import api from '@/utils/axios'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()

// State
const photos = ref([])
const loadingPhotos = ref(false)
const showUploadModal = ref(false)
const uploadingPhoto = ref(false)
const photoForm = ref({
    title: '',
    category: 'EVENT',
    image: null
})

const uploadLabel = computed(() => {
    return photoForm.value.image ? photoForm.value.image.name : 'Télécharger un fichier'
})

// Methods
const fetchPhotos = async () => {
    loadingPhotos.value = true
    try {
        const res = await api.get('/api/gallery/')
        photos.value = res.data.results || res.data
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors du chargement des photos")
    } finally {
        loadingPhotos.value = false
    }
}

const imagePreview = ref(null)

const handleFileChange = (event) => {
    const file = event.target.files[0]
    if (file) {
        photoForm.value.image = file
        imagePreview.value = URL.createObjectURL(file)
    }
}

const openUploadModal = () => {
    photoForm.value = {
        title: '',
        category: 'EVENT',
        image: null
    }
    imagePreview.value = null
    showUploadModal.value = true
}

const uploadPhoto = async () => {
    if (!photoForm.value.image) {
        toast.error("Veuillez sélectionner une image")
        return
    }

    uploadingPhoto.value = true
    // toast.info("Envoi en cours...") // Optional feedback
    const formData = new FormData()
    formData.append('title', photoForm.value.title)
    formData.append('category', photoForm.value.category)
    formData.append('image', photoForm.value.image)

    try {
        await api.post('/api/gallery/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        toast.success("Photo téléchargée avec succès")
        showUploadModal.value = false
        await fetchPhotos()
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors du téléchargement")
    } finally {
        uploadingPhoto.value = false
    }
}

const deletePhoto = async (id) => {
    if (!confirm("Êtes-vous sûr de vouloir supprimer cette photo ?")) return

    try {
        await api.delete(`/api/gallery/${id}/`)
        toast.success("Photo supprimée")
        await fetchPhotos()
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de la suppression")
    }
}

const getCategoryLabel = (category) => {
    const labels = {
        'EVENT': 'Événement',
        'COMPETITION': 'Compétition',
        'INTERNSHIP': 'Stage',
        'OTHER': 'Autre'
    }
    return labels[category] || category
}

onMounted(() => {
    fetchPhotos()
})
</script>

<template>
    <div>
        <div class="flex justify-between items-center mb-6">
            <div>
                <h2 class="text-2xl font-bold text-gray-900">Galerie Photos</h2>
                <p class="text-gray-500">Gérer les photos du site web</p>
            </div>
            <BaseButton variant="primary" @click="openUploadModal">
                <template #icon>
                    <Upload :size="20" />
                </template>
                Ajouter une photo
            </BaseButton>
        </div>

        <div v-if="loadingPhotos" class="flex justify-center py-20">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-judo-blue"></div>
        </div>

        <div v-else-if="photos.length === 0"
            class="text-center py-20 bg-white rounded-lg border border-dashed border-gray-300">
            <ImageIcon :size="48" class="mx-auto text-gray-300 mb-4" />
            <p class="text-gray-500">Aucune photo dans la galerie</p>
            <BaseButton variant="primary" class="mt-4" @click="openUploadModal">
                Télécharger une première photo
            </BaseButton>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <div v-for="photo in photos" :key="photo.id"
                class="group relative bg-white rounded-lg shadow-sm overflow-hidden border border-gray-100 hover:shadow-md transition">
                <div class="aspect-w-16 aspect-h-9 bg-gray-100 relative">
                    <img :src="photo.image" :alt="photo.title" class="object-cover w-full h-48" />
                    <div
                        class="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-colors flex items-center justify-center opacity-0 group-hover:opacity-100">
                        <button @click="deletePhoto(photo.id)"
                            class="bg-white/90 p-2 rounded-full text-red-600 hover:bg-red-50 transition transform hover:scale-110">
                            <Trash2 :size="20" />
                        </button>
                    </div>
                </div>
                <div class="p-4">
                    <h3 class="font-bold text-gray-900 truncate">{{ photo.title }}</h3>
                    <span class="inline-block mt-1 px-2 py-0.5 rounded text-xs font-medium bg-blue-50 text-blue-700">
                        {{ getCategoryLabel(photo.category) }}
                    </span>
                    <p class="text-xs text-gray-400 mt-2">
                        {{ new Date(photo.created_at).toLocaleDateString() }}
                    </p>
                </div>
            </div>
        </div>

        <!-- Upload Modal -->
        <div v-if="showUploadModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title"
            role="dialog" aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                    @click="showUploadModal = false"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div
                    class="flex align-bottom bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-100 max-h-[90vh] flex-col">
                    <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 overflow-y-auto">
                        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
                            Ajouter une photo
                        </h3>
                        <form @submit.prevent="uploadPhoto" class="space-y-4">
                            <BaseInput id="photo-title" label="Titre" v-model="photoForm.title" required
                                placeholder="Ex: Compétition Régionale" />

                            <div>
                                <BaseSelect id="photo-category" label="Catégorie" v-model="photoForm.category">
                                    <option value="EVENT">Événement</option>
                                    <option value="COMPETITION">Compétition</option>
                                    <option value="INTERNSHIP">Stage</option>
                                    <option value="OTHER">Autre</option>
                                </BaseSelect>
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Image</label>
                                <div
                                    class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-judo-blue transition-colors cursor-pointer relative">
                                    <div class="space-y-1 text-center">
                                        <div v-if="imagePreview" class="mb-3">
                                            <img :src="imagePreview" class="mx-auto h-32 object-contain rounded-md" />
                                        </div>
                                        <ImageIcon v-else class="mx-auto h-12 w-12 text-gray-400" />

                                        <div class="flex text-sm text-gray-600 justify-center">
                                            <label for="file-upload"
                                                class="relative cursor-pointer bg-white rounded-md font-medium text-judo-blue hover:text-blue-500 focus-within:outline-none">
                                                <span>{{ imagePreview ? 'Changer l\'image' : 'Télécharger un fichier'
                                                }}</span>
                                                <input id="file-upload" name="file-upload" type="file" class="sr-only"
                                                    @change="handleFileChange" accept="image/*" />
                                            </label>
                                        </div>
                                        <p class="text-xs text-gray-500">PNG, JPG, GIF jusqu'à 5MB</p>
                                    </div>
                                </div>
                            </div>

                            <div
                                class="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-3 space-y-3 space-y-reverse sm:space-y-0 mt-6 sticky bottom-0 bg-white pt-2">
                                <BaseButton type="button" variant="white" @click="showUploadModal = false"
                                    class="w-full sm:w-auto">
                                    Annuler
                                </BaseButton>
                                <BaseButton type="button" variant="primary" :loading="uploadingPhoto"
                                    @click="uploadPhoto" class="w-full sm:w-auto">
                                    Valider la photo
                                </BaseButton>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

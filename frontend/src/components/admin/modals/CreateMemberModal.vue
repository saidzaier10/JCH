<script setup>
import { ref, computed, onMounted } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import api from '@/utils/axios'
import { useToastStore } from '@/stores/toast'
import { getWeightCategories } from '@/utils/judo-weights'

const props = defineProps({
    isOpen: {
        type: Boolean,
        required: true
    }
})

const emit = defineEmits(['close', 'created'])

const toast = useToastStore()
const creatingMember = ref(false)
const loadingParents = ref(false)
const parents = ref([])

const form = ref({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    birth_date: '',
    license_number: '',
    address: '',
    gender: 'M',
    weight_category: '',
    discipline: 'JUDO',
    belt: 'WHITE',
    image_rights: false,
    medical_certificate_valid_until: null,
    parent: null // ID of the parent user
})

const fetchParents = async () => {
    loadingParents.value = true
    try {
        // We need an endpoint to get users. Assuming standard DRF User endpoint helps, 
        // but often we might need a custom query to get "potential parents". 
        // For now, let's assume we can GET /api/users/ (we might need to create this viewset if not exists)
        // Or checking implementation plan, we might need to add a way to list users.
        // Let's assume we use the UsersTab logic.
        const response = await api.get('/api/users/') // We need to check if this exists
        parents.value = response.data.results || response.data
    } catch (e) {
        console.error("Error fetching parents:", e)
        toast.error("Impossible de charger la liste des parents")
    } finally {
        loadingParents.value = false
    }
}

onMounted(() => {
    if (props.isOpen) {
        fetchParents()
    }
})

// Watch isOpen to fetch parents when modal opens
import { watch } from 'vue'
watch(() => props.isOpen, (newVal) => {
    if (newVal && parents.value.length === 0) {
        fetchParents()
    }
})

const weightChoices = computed(() => {
    if (!form.value.birth_date) return []
    return getWeightCategories(form.value.birth_date, form.value.gender)
})

const create = async () => {
    creatingMember.value = true
    try {
        await api.post('/api/members/', form.value)
        toast.success('Membre créé avec succès')
        emit('created')
        emit('close')
        // Reset form
        form.value = {
            first_name: '',
            last_name: '',
            email: '',
            phone: '',
            birth_date: '',
            license_number: '',
            address: '',
            gender: 'M',
            weight_category: '',
            discipline: 'JUDO',
            belt: 'WHITE',
            image_rights: false,
            medical_certificate_valid_until: null,
            parent: null
        }
    } catch (e) {
        console.error("Error creating member:", e)
        toast.error("Erreur lors de la création du membre")
    } finally {
        creatingMember.value = false
    }
}
</script>

<template>
    <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog"
        aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                @click="$emit('close')"></div>
            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div
                class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
                        Ajouter un nouveau membre
                    </h3>
                    <form @submit.prevent="create" class="space-y-5">

                        <!-- Parent Selection -->
                        <div class="bg-blue-50 p-4 rounded-lg mb-4">
                            <label class="block text-sm font-medium text-blue-900 mb-2">Compte Parent Associé</label>
                            <BaseSelect v-model="form.parent" :disabled="loadingParents" required>
                                <option :value="null">Sélectionner un parent...</option>
                                <option v-for="parent in parents" :key="parent.id" :value="parent.id">
                                    {{ parent.first_name }} {{ parent.last_name }} ({{ parent.username }})
                                </option>
                            </BaseSelect>
                            <p v-if="loadingParents" class="text-xs text-blue-500 mt-1">Chargement des parents...</p>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <BaseInput id="new-firstname" label="Prénom" v-model="form.first_name" required />
                            <BaseInput id="new-lastname" label="Nom" v-model="form.last_name" required />
                        </div>
                        <BaseInput id="new-email" label="Email (Optionnel)" type="email" v-model="form.email" />
                        <BaseInput id="new-phone" label="Téléphone (Optionnel)" v-model="form.phone" />

                        <div class="grid grid-cols-2 gap-4">
                            <BaseInput id="new-birthdate" label="Date de naissance" type="date"
                                v-model="form.birth_date" required />

                            <BaseSelect label="Genre" v-model="form.gender">
                                <option value="M">Masculin</option>
                                <option value="F">Féminin</option>
                            </BaseSelect>
                        </div>
                        <BaseInput id="new-license" label="Numéro de licence" v-model="form.license_number" />
                        <BaseInput id="new-address" label="Adresse" v-model="form.address" />

                        <div>
                            <BaseSelect label="Catégorie de poids" v-model="form.weight_category">
                                <option value="">Sélectionner une catégorie...</option>
                                <option v-for="option in weightChoices" :key="option.value" :value="option.value">
                                    {{ option.label }}
                                </option>
                            </BaseSelect>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <BaseSelect label="Discipline" v-model="form.discipline">
                                    <option value="EVEIL">Judo Éveil</option>
                                    <option value="JUDO">Judo</option>
                                    <option value="TAISO">Taïso</option>
                                    <option value="TAISO_SENIOR">Taïso Senior</option>
                                    <option value="APA">Activité Physique Adaptée</option>
                                    <option value="JUJITSU">Ju-Jitsu</option>
                                </BaseSelect>
                            </div>
                            <div>
                                <BaseSelect label="Ceinture" v-model="form.belt">
                                    <option value="WHITE">Blanche</option>
                                    <option value="WHITE_YELLOW">Blanche-Jaune</option>
                                    <option value="YELLOW">Jaune</option>
                                    <option value="YELLOW_ORANGE">Jaune-Orange</option>
                                    <option value="ORANGE">Orange</option>
                                    <option value="ORANGE_GREEN">Orange-Verte</option>
                                    <option value="GREEN">Verte</option>
                                    <option value="BLUE">Bleue</option>
                                    <option value="BROWN">Marron</option>
                                    <option value="BLACK">Noire</option>
                                </BaseSelect>
                            </div>
                        </div>

                        <div class="flex items-center">
                            <input id="new_image_rights" v-model="form.image_rights" type="checkbox"
                                class="h-4 w-4 text-judo-blue focus:ring-judo-blue border-gray-300 rounded">
                            <label for="new_image_rights" class="ml-2 block text-sm text-gray-900">
                                Autorisation Droit à l'image
                            </label>
                        </div>

                        <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                            <BaseButton type="submit" variant="primary" :loading="creatingMember"
                                class="w-full sm:col-start-2">
                                Créer Membre
                            </BaseButton>
                            <BaseButton type="button" variant="white" @click="$emit('close')"
                                class="mt-3 w-full sm:mt-0 sm:col-start-1">
                                Annuler
                            </BaseButton>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

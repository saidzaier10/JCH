<script setup>
import { ref, watch, computed } from 'vue'
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
    },
    member: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['close', 'saved'])

const toast = useToastStore()
const updatingMember = ref(false)

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
    medical_certificate_valid_until: null
})

watch(() => props.member, (newMember) => {
    if (newMember) {
        form.value = {
            first_name: newMember.first_name,
            last_name: newMember.last_name,
            email: newMember.email,
            phone: newMember.phone,
            birth_date: newMember.birth_date,
            license_number: newMember.license_number,
            address: newMember.address,
            gender: newMember.gender,
            weight_category: newMember.weight_category || '',
            discipline: newMember.discipline || 'JUDO',
            belt: newMember.belt || 'WHITE',
            image_rights: newMember.image_rights || false,
            medical_certificate_valid_until: newMember.medical_certificate_valid_until
        }
    }
}, { immediate: true })

const weightChoices = computed(() => {
    if (!form.value.birth_date) return []
    return getWeightCategories(form.value.birth_date, form.value.gender)
})

const save = async () => {
    updatingMember.value = true
    try {
        await api.patch(`/api/members/${props.member.id}/`, form.value)
        toast.success('Membre mis à jour avec succès')
        emit('saved')
        emit('close')
    } catch (e) {
        console.error("Error updating member:", e)
        toast.error("Erreur lors de la mise à jour du membre")
    } finally {
        updatingMember.value = false
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
                    <h3 class="text-lg leading-6 font-bold text-gray-900 mb-4" id="modal-title">
                        Modifier le membre : <span class="text-judo-blue">{{ member.first_name }} {{ member.last_name
                        }}</span>
                    </h3>
                    <form @submit.prevent="save" class="space-y-5">
                        <div class="grid grid-cols-2 gap-4">
                            <BaseInput id="edit-firstname" label="Prénom" v-model="form.first_name" required />
                            <BaseInput id="edit-lastname" label="Nom" v-model="form.last_name" required />
                        </div>
                        <BaseInput id="edit-email" label="Email" type="email" v-model="form.email" />
                        <BaseInput id="edit-phone" label="Téléphone" v-model="form.phone" />

                        <div class="grid grid-cols-2 gap-4">
                            <BaseInput id="edit-birthdate" label="Date de naissance" type="date"
                                v-model="form.birth_date" required />

                            <BaseSelect label="Genre" v-model="form.gender">
                                <option value="M">Masculin</option>
                                <option value="F">Féminin</option>
                            </BaseSelect>
                        </div>
                        <BaseInput id="edit-license" label="Numéro de licence" v-model="form.license_number" />
                        <BaseInput id="edit-address" label="Adresse" v-model="form.address" />

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
                            <input id="edit_image_rights" v-model="form.image_rights" type="checkbox"
                                class="h-4 w-4 text-judo-blue focus:ring-judo-blue border-gray-300 rounded">
                            <label for="edit_image_rights" class="ml-2 block text-sm text-gray-900">
                                Autorisation Droit à l'image
                            </label>
                        </div>

                        <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                            <BaseButton type="submit" variant="primary" :loading="updatingMember"
                                class="w-full sm:col-start-2">
                                Enregistrer
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

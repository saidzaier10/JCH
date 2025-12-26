<script setup>
import { ref, watch } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseListbox from '@/components/ui/BaseListbox.vue'
import api from '@/utils/axios'
import { useToastStore } from '@/stores/toast'
import { ALL_WEIGHTS } from '@/utils/judo-weights'

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
const savingWeight = ref(false)
const form = ref({
    weight_category: ''
})

watch(() => props.member, (newMember) => {
    if (newMember) {
        form.value = {
            weight_category: newMember.weight_category || ''
        }
    }
}, { immediate: true })

const save = async () => {
    savingWeight.value = true
    try {
        await api.patch(`/api/members/${props.member.id}/`, {
            weight_category: form.value.weight_category
        })
        toast.success("Catégorie de poids mise à jour")
        emit('saved')
        emit('close')
    } catch (e) {
        console.error(e)
        const errorMsg = e.response?.data?.detail || "Erreur lors de la mise à jour."
        toast.error(errorMsg)
    } finally {
        savingWeight.value = false
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
                class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-100">
                <div class="bg-white px-6 pt-6 pb-6">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-xl font-bold text-gray-900" id="modal-title">
                            Pesée - {{ member?.first_name }} {{ member?.last_name }}
                        </h3>
                        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-500">
                            <span class="sr-only">Fermer</span>
                            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                    <form @submit.prevent="save" class="space-y-6">
                        <div>
                            <BaseListbox v-model="form.weight_category" :options="ALL_WEIGHTS"
                                label="Catégorie de poids" placeholder="Sélectionner une catégorie..." />
                        </div>

                        <div
                            class="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-3 space-y-3 space-y-reverse sm:space-y-0">
                            <BaseButton type="button" variant="white" @click="$emit('close')" class="w-full sm:w-auto">
                                Annuler
                            </BaseButton>
                            <BaseButton type="submit" variant="primary" :loading="savingWeight"
                                class="w-full sm:w-auto">
                                Enregistrer
                            </BaseButton>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

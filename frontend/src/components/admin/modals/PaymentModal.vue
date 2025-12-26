<script setup>
import { ref, watch } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import api from '@/utils/axios'
import { useToastStore } from '@/stores/toast'

const props = defineProps({
    isOpen: {
        type: Boolean,
        required: true
    },
    registration: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['close', 'saved'])

const toast = useToastStore()
const savingPayment = ref(false)

const form = ref({
    payment_mode: 'FULL',
    installments_paid: 0,
    paid: false
})

watch(() => props.registration, (newReg) => {
    if (newReg) {
        form.value = {
            payment_mode: newReg.payment_mode || 'FULL',
            installments_paid: newReg.installments_paid || 0,
            paid: newReg.paid
        }
    }
}, { immediate: true })

const updateInstallments = (level) => {
    if (form.value.installments_paid >= level) {
        form.value.installments_paid = level - 1
    } else {
        form.value.installments_paid = level
    }
}

const save = async () => {
    savingPayment.value = true

    // Auto-calculate paid status
    let isPaid = form.value.paid
    if (form.value.payment_mode === '3X') {
        isPaid = form.value.installments_paid >= 3
    }

    try {
        await api.patch(`/api/registrations/${props.registration.id}/`, {
            payment_mode: form.value.payment_mode,
            installments_paid: form.value.installments_paid,
            paid: isPaid
        })
        toast.success("Paiement mis à jour")
        emit('saved')
        emit('close')
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de la mise à jour du paiement")
    } finally {
        savingPayment.value = false
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
                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
                        Gérer le paiement
                    </h3>
                    <p class="text-sm text-gray-500 mb-4">
                        Adhérent : {{ registration.member.first_name }} {{ registration.member.last_name }}
                    </p>

                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Mode de paiement</label>
                            <div class="flex space-x-4 mt-2">
                                <label class="inline-flex items-center">
                                    <input type="radio" class="form-radio text-judo-blue" value="FULL"
                                        v-model="form.payment_mode">
                                    <span class="ml-2">Comptant</span>
                                </label>
                                <label class="inline-flex items-center">
                                    <input type="radio" class="form-radio text-judo-blue" value="3X"
                                        v-model="form.payment_mode">
                                    <span class="ml-2">3 Fois</span>
                                </label>
                            </div>
                        </div>

                        <div v-if="form.payment_mode === '3X'" class="bg-gray-50 p-4 rounded-lg">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Suivi des mensualités</label>
                            <div class="space-y-2">
                                <label class="flex items-center">
                                    <input type="checkbox" class="form-checkbox text-judo-blue"
                                        :checked="form.installments_paid >= 1" @change="updateInstallments(1)">
                                    <span class="ml-2">1ère mensualité</span>
                                </label>
                                <label class="flex items-center">
                                    <input type="checkbox" class="form-checkbox text-judo-blue"
                                        :checked="form.installments_paid >= 2" @change="updateInstallments(2)">
                                    <span class="ml-2">2ème mensualité</span>
                                </label>
                                <label class="flex items-center">
                                    <input type="checkbox" class="form-checkbox text-judo-blue"
                                        :checked="form.installments_paid >= 3" @change="updateInstallments(3)">
                                    <span class="ml-2">3ème mensualité</span>
                                </label>
                            </div>
                        </div>

                        <div v-else>
                            <label class="flex items-center mt-4">
                                <input type="checkbox" class="form-checkbox text-judo-blue" v-model="form.paid">
                                <span class="ml-2 font-medium">Marquer comme payé</span>
                            </label>
                        </div>
                    </div>

                    <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                        <BaseButton variant="primary" @click="save" :loading="savingPayment"
                            class="w-full sm:col-start-2">
                            Enregistrer
                        </BaseButton>
                        <BaseButton variant="white" @click="$emit('close')" class="mt-3 w-full sm:mt-0 sm:col-start-1">
                            Annuler
                        </BaseButton>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

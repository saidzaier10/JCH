<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
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
const form = ref({
    discount_percentage: 0,
    discount_amount: 0,
    has_supplementary_discipline: false,
    city_hall_aid: false,
    city_hall_aid_amount: 0
})

const basePrice = computed(() => {
    return parseFloat(props.registration?.category?.price || 0)
})

const calculatedDiscount = computed(() => {
    let discount = 0
    if (form.value.discount_percentage > 0) {
        discount += (basePrice.value * form.value.discount_percentage) / 100
    }
    if (form.value.discount_amount > 0) {
        discount += parseFloat(form.value.discount_amount)
    }
    return discount
})

const finalPrice = computed(() => {
    let price = basePrice.value

    // Add Supplements
    if (form.value.has_supplementary_discipline) {
        price += 40
    }

    // Deduct Discount
    price -= calculatedDiscount.value

    // Deduct Aid
    if (form.value.city_hall_aid && form.value.city_hall_aid_amount > 0) {
        price -= parseFloat(form.value.city_hall_aid_amount)
    }

    return Math.max(0, price)
})

watch(() => props.registration, (newReg) => {
    if (newReg) {
        form.value = {
            discount_percentage: parseFloat(newReg.discount_percentage || 0),
            discount_amount: parseFloat(newReg.discount_amount || 0),
            has_supplementary_discipline: newReg.has_supplementary_discipline || false,
            city_hall_aid: newReg.city_hall_aid || false,
            city_hall_aid_amount: parseFloat(newReg.city_hall_aid_amount || 0)
        }
    }
}, { immediate: true })

const save = async () => {
    try {
        await api.patch(`/api/registrations/${props.registration.id}/`, form.value)
        toast.success("Tarif mis à jour avec succès")
        emit('saved')
        emit('close')
    } catch (e) {
        console.error(e)
        const errorMsg = e.response?.data?.detail || "Erreur lors de la mise à jour du tarif"
        toast.error(errorMsg)
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
                    <div class="sm:flex sm:items-start space-x-6">
                        <!-- Form Section -->
                        <div class="flex-1 text-center sm:text-left">
                            <h3 class="text-lg leading-6 font-bold text-gray-900" id="modal-title">
                                Modifier le tarif : <span class="text-judo-blue">{{ registration.member.first_name }} {{
                                    registration.member.last_name }}</span>
                            </h3>
                            <div class="mt-2 text-left">
                                <p class="text-sm text-gray-500 mb-4">
                                    Ajustements pour {{ registration.member.first_name }}
                                </p>

                                <div class="space-y-4">
                                    <BaseInput type="number" v-model="form.discount_percentage"
                                        label="Remise en pourcentage (%)" min="0" max="100" step="0.01" />

                                    <BaseInput type="number" v-model="form.discount_amount" label="Remise fixe (€)"
                                        min="0" step="0.01" />

                                    <div class="border-t pt-4 mt-4">
                                        <h4 class="font-medium text-gray-900 mb-2">Options & Aides</h4>
                                        <div class="space-y-3">
                                            <div class="flex items-center p-3 bg-gray-50 rounded-lg">
                                                <input id="admin_supp_discipline"
                                                    v-model="form.has_supplementary_discipline" type="checkbox"
                                                    class="h-5 w-5 text-judo-blue focus:ring-judo-blue border-gray-300 rounded cursor-pointer">
                                                <div class="ml-3">
                                                    <label for="admin_supp_discipline"
                                                        class="block text-sm font-medium text-gray-900 cursor-pointer">
                                                        Discipline supplémentaire
                                                    </label>
                                                    <span class="text-xs text-gray-500">+40.00 €</span>
                                                </div>
                                            </div>

                                            <div class="flex items-center p-3 bg-gray-50 rounded-lg">
                                                <input id="admin_city_aid" v-model="form.city_hall_aid" type="checkbox"
                                                    class="h-5 w-5 text-judo-blue focus:ring-judo-blue border-gray-300 rounded cursor-pointer">
                                                <div class="ml-3">
                                                    <label for="admin_city_aid"
                                                        class="block text-sm font-medium text-gray-900 cursor-pointer">
                                                        Aide Mairie / Pass'Sport
                                                    </label>
                                                    <span class="text-xs text-gray-500">Déduction du montant de
                                                        l'aide</span>
                                                </div>
                                            </div>

                                            <div v-if="form.city_hall_aid"
                                                class="ml-2 pl-4 border-l-2 border-judo-blue">
                                                <BaseInput type="number" v-model="form.city_hall_aid_amount"
                                                    label="Montant de l'aide (€)" min="0" step="1" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Summary Section -->
                        <div class="w-full sm:w-72 bg-gray-50 rounded-xl p-6 h-fit border border-gray-200 mt-6 sm:mt-0">
                            <h4 class="font-bold text-gray-900 mb-4 border-b pb-2">Résumé du calcul</h4>
                            <div class="space-y-3 text-sm">
                                <div class="flex justify-between">
                                    <span class="text-gray-600">Prix de base ({{ registration.category.name }})</span>
                                    <span class="font-medium">{{ basePrice.toFixed(2) }} €</span>
                                </div>
                                <div v-if="form.has_supplementary_discipline"
                                    class="flex justify-between text-blue-700">
                                    <span>Discipline suppl.</span>
                                    <span>+40.00 €</span>
                                </div>
                                <div v-if="calculatedDiscount > 0" class="flex justify-between text-green-700">
                                    <span>Remise</span>
                                    <span>-{{ calculatedDiscount.toFixed(2) }} €</span>
                                </div>
                                <div v-if="form.city_hall_aid && form.city_hall_aid_amount > 0"
                                    class="flex justify-between text-green-700">
                                    <span>Aide Mairie</span>
                                    <span>-{{ form.city_hall_aid_amount }} €</span>
                                </div>
                                <div class="pt-3 border-t border-gray-200 flex justify-between items-center mt-2">
                                    <span class="font-bold text-gray-900">Total à payer</span>
                                    <span class="text-xl font-extrabold text-judo-blue">{{ finalPrice.toFixed(2) }}
                                        €</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                    <BaseButton variant="primary" @click="save" class="w-full sm:w-auto sm:ml-3">
                        Enregistrer
                    </BaseButton>
                    <BaseButton variant="white" @click="$emit('close')" class="mt-3 w-full sm:mt-0 sm:w-auto">
                        Annuler
                    </BaseButton>
                </div>
            </div>
        </div>
    </div>
</template>

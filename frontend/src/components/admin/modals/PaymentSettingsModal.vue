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
                    <h3 class="text-lg leading-6 font-bold text-gray-900 mb-4" id="modal-title">
                        Paramètres de Paiement
                    </h3>

                    <div v-if="loading" class="flex justify-center py-4">
                        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-judo-blue"></div>
                    </div>

                    <div v-else>
                        <!-- List -->
                        <div class="space-y-3 mb-6">
                            <h4 class="text-sm font-medium text-gray-700">Options existantes</h4>
                            <div v-for="option in options" :key="option.id"
                                class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div>
                                    <p class="font-medium text-gray-900">{{ option.name }}</p>
                                    <p class="text-xs text-gray-500">{{ option.installments }} échéance(s)</p>
                                </div>
                                <div class="flex items-center space-x-2">
                                    <span v-if="option.is_active" class="h-2 w-2 rounded-full bg-green-500"></span>
                                    <span v-else class="h-2 w-2 rounded-full bg-red-500"></span>
                                    <button @click="deleteOption(option.id)"
                                        class="text-red-600 hover:text-red-900 ml-2">
                                        <Trash2 :size="16" />
                                    </button>
                                </div>
                            </div>
                            <p v-if="options.length === 0" class="text-sm text-gray-500 italic">Aucune option définie.
                            </p>
                        </div>

                        <!-- Add Form -->
                        <div class="border-t pt-4">
                            <h4 class="text-sm font-medium text-gray-700 mb-3">Ajouter une option</h4>
                            <form @submit.prevent="createOption" class="space-y-3">
                                <BaseInput v-model="newOption.name" label="Nom" placeholder="Ex: 3 Fois sans frais"
                                    required />
                                <BaseInput v-model="newOption.installments" type="number" label="Nombre d'échéances"
                                    min="1" max="12" required />
                                <div class="flex items-center">
                                    <input type="checkbox" id="is_active_opt" v-model="newOption.is_active"
                                        class="h-4 w-4 text-judo-blue focus:ring-judo-blue border-gray-300 rounded">
                                    <label for="is_active_opt" class="ml-2 block text-sm text-gray-900">Active</label>
                                </div>
                                <BaseButton type="submit" variant="primary" :loading="creating" class="w-full mt-2">
                                    Ajouter
                                </BaseButton>
                            </form>
                        </div>
                    </div>

                    <div class="mt-6 flex justify-end">
                        <BaseButton variant="white" @click="$emit('close')">Fermer</BaseButton>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Trash2 } from 'lucide-vue-next'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import api from '@/utils/axios'
import { useToastStore } from '@/stores/toast'

const props = defineProps({
    isOpen: Boolean
})

const emit = defineEmits(['close'])
const toast = useToastStore()

const options = ref([])
const loading = ref(false)
const creating = ref(false)

const newOption = ref({
    name: '',
    installments: 1,
    is_active: true
})

const fetchOptions = async () => {
    loading.value = true
    try {
        const res = await api.get('/api/payment-options/')
        options.value = res.data.results || res.data
    } catch (e) {
        console.error(e)
        toast.error("Erreur chargement options")
    } finally {
        loading.value = false
    }
}

const createOption = async () => {
    creating.value = true
    try {
        await api.post('/api/payment-options/', newOption.value)
        toast.success("Option créée")
        newOption.value = { name: '', installments: 1, is_active: true }
        await fetchOptions()
    } catch (e) {
        console.error(e)
        toast.error("Erreur création")
    } finally {
        creating.value = false
    }
}

const deleteOption = async (id) => {
    if (!confirm("Supprimer cette option ?")) return
    try {
        await api.delete(`/api/payment-options/${id}/`)
        toast.success("Option supprimée")
        await fetchOptions()
    } catch (e) {
        console.error(e)
        toast.error("Impossible de supprimer (probablement utilisée)")
    }
}

onMounted(() => {
    if (props.isOpen) fetchOptions()
})
// Watch isOpen to refetch if opened again? 
// Simplification: just fetch on mount or we can watch props.isOpen
import { watch } from 'vue'
watch(() => props.isOpen, (newVal) => {
    if (newVal) fetchOptions()
})
</script>

<script setup>
import { ref, watch } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import api from '@/utils/axios'
import { useToastStore } from '@/stores/toast'

const props = defineProps({
    isOpen: {
        type: Boolean,
        required: true
    },
    user: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['close', 'updated'])

const toast = useToastStore()
const loading = ref(false)
const form = ref({
    username: '',
    email: '',
    is_active: true
})

// Populate form when user changes
watch(() => props.user, (newUser) => {
    if (newUser) {
        form.value = {
            username: newUser.username,
            email: newUser.email,
            is_active: newUser.is_active
        }
    }
}, { immediate: true })

const saveUser = async () => {
    if (!props.user) return

    loading.value = true
    try {
        await api.patch(`/api/users/${props.user.id}/`, form.value)
        toast.success(`Utilisateur "${form.value.username}" mis à jour !`)
        emit('updated')
        emit('close')
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de la mise à jour de l'utilisateur")
    } finally {
        loading.value = false
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
                        Modifier l'utilisateur : {{ user?.username }}
                    </h3>
                    <form @submit.prevent="saveUser" class="space-y-4">
                        <BaseInput id="edit-username" label="Nom d'utilisateur" v-model="form.username" required />
                        <BaseInput id="edit-email" label="Email" type="email" v-model="form.email" />

                        <div class="flex items-center mt-4">
                            <input type="checkbox" id="is_active" v-model="form.is_active"
                                class="h-4 w-4 text-judo-blue focus:ring-judo-blue border-gray-300 rounded">
                            <label for="is_active" class="ml-2 block text-sm text-gray-900">Compte actif</label>
                        </div>

                        <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                            <BaseButton type="submit" variant="primary" :loading="loading"
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

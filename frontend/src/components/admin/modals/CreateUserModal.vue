<script setup>
import { ref } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import api from '@/utils/axios'
import { useToastStore } from '@/stores/toast'

const props = defineProps({
    isOpen: {
        type: Boolean,
        required: true
    }
})

const emit = defineEmits(['close', 'created'])

const toast = useToastStore()
const loadingUser = ref(false)
const userForm = ref({
    username: '',
    email: '',
    password: ''
})

const createUser = async () => {
    loadingUser.value = true
    try {
        await api.post('/api/register/', userForm.value)
        toast.success(`Compte parent "${userForm.value.username}" créé avec succès !`)
        userForm.value = { username: '', email: '', password: '' }
        emit('created')
        emit('close')
    } catch (e) {
        console.error(e)
        // Error handling is handled by axios interceptor usually, but toast here for safe measure?
        // Actually axios interceptor handled it in previous code, but here we can be explicit if needed.
    } finally {
        loadingUser.value = false
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
                        Créer un compte Parent
                    </h3>
                    <form @submit.prevent="createUser" class="space-y-4">
                        <BaseInput id="new-username" label="Nom d'utilisateur" v-model="userForm.username" required
                            placeholder="ex: dupont_famille" />
                        <BaseInput id="new-email" label="Email (Optionnel)" type="email" v-model="userForm.email"
                            placeholder="ex: contact@famille.com" />
                        <BaseInput id="new-password" label="Mot de passe" type="password" v-model="userForm.password"
                            required placeholder="********" />

                        <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                            <BaseButton type="submit" variant="primary" :loading="loadingUser"
                                class="w-full sm:col-start-2">
                                Créer le compte
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

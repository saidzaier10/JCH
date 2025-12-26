<script setup>
import { ref } from 'vue'
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/utils/axios'
import { useSeo } from '../composables/useSeo'

import { useToastStore } from '../stores/toast'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()
const route = useRoute()
const isAdminLogin = computed(() => route.name === 'admin-login')

useSeo(isAdminLogin.value ? 'Connexion Admin' : 'Connexion Famille', 'Connectez-vous à votre espace.')
const toast = useToastStore()
const username = ref('')
const password = ref('')
const loading = ref(false)

const handleLogin = async () => {
    loading.value = true

    try {
        const response = await api.post('/api/token/', {
            username: username.value,
            password: password.value
        })

        // Store tokens
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        localStorage.setItem('username', username.value)
        localStorage.setItem('is_staff', response.data.is_staff)

        toast.success(`Bienvenue ${username.value} !`)

        // Redirect based on role
        // Redirect based on role and login context
        if (isAdminLogin.value) {
            if (response.data.is_staff) {
                router.push('/dashboard')
            } else {
                toast.warning("Vous n'avez pas les droits d'administration. Redirection vers l'espace famille.")
                router.push('/my-space')
            }
        } else {
            // Parent login
            if (response.data.is_staff) {
                // Staff logging in via parent portal -> redirect to dashboard anyway or keep in my-space?
                // Let's redirect to dashboard for convenience, or ask them?
                // For now, standard behavior:
                router.push('/dashboard')
            } else {
                router.push('/my-space')
            }
        }

    } catch (err) {
        console.error(err)
        toast.error("Identifiants incorrects. Veuillez réessayer.")
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div
        class="min-h-screen flex items-center justify-center bg-linear-to-br from-gray-900 via-blue-900 to-judo-blue py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">

        <!-- Decorative background elements -->
        <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
            <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
            <div
                class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl animate-pulse delay-1000">
            </div>
        </div>

        <BaseCard variant="glass" class="max-w-md w-full relative z-10 p-0">
            <div class="px-8 pt-8 pb-6 text-center">
                <div class="mx-auto h-20 w-20 rounded-2xl flex items-center justify-center shadow-xl mb-6 transform transition-transform hover:scale-110"
                    :class="isAdminLogin ? 'bg-linear-to-br from-blue-600 to-blue-800' : 'bg-linear-to-br from-emerald-500 to-emerald-700'">
                    <span class="text-4xl filter drop-shadow-md">{{ isAdminLogin ? '🥋' : '👨‍👩‍👧‍👦' }}</span>
                </div>
                <h2 class="text-3xl font-extrabold text-white tracking-tight">
                    {{ isAdminLogin ? 'Espace Club' : 'Espace Famille' }}
                </h2>
                <p class="mt-2 text-blue-100 font-light">
                    {{ isAdminLogin ? "Gestion administrative" : "Gérez les inscriptions de vos enfants" }}
                </p>
            </div>

            <div class="px-8 pb-10">
                <form class="space-y-6" @submit.prevent="handleLogin">
                    <div class="space-y-4">
                        <BaseInput id="username" label="Identifiant" v-model="username" required
                            placeholder="Votre identifiant" variant="glass">
                            <template #prefix>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-200" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                            </template>
                        </BaseInput>

                        <BaseInput id="password" type="password" label="Mot de passe" v-model="password" required
                            placeholder="Votre mot de passe" variant="glass">
                            <template #prefix>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-200" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                            </template>
                        </BaseInput>
                    </div>

                    <div class="pt-2">
                        <BaseButton type="submit" variant="primary" :loading="loading" block
                            class="w-full bg-linear-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 shadow-lg hover:shadow-blue-500/50 border-none h-12 text-lg font-semibold">
                            {{ loading ? 'Connexion...' : 'Se connecter' }}
                            <template #icon v-if="!loading">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                                </svg>
                            </template>
                        </BaseButton>
                    </div>
                </form>
            </div>

            <div class="px-8 py-4 bg-black/20 text-center rounded-b-2xl border-t border-white/5">
                <p class="text-sm text-blue-200">
                    Pas encore de compte ?
                    <router-link to="/signup"
                        class="font-bold text-white hover:text-blue-300 underline decoration-blue-400 decoration-2 underline-offset-4">
                        Créer un compte
                    </router-link>
                </p>
            </div>
        </BaseCard>
    </div>
</template>

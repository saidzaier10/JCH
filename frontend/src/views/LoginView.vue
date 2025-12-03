<script setup>
import { ref } from 'vue'
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/utils/axios'
import { useSeo } from '../composables/useSeo'

import { useToastStore } from '../stores/toast'

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
        class="min-h-screen flex items-center justify-center bg-linear-to-br from-gray-900 to-judo-blue py-12 px-4 sm:px-6 lg:px-8">
        <div
            class="max-w-md w-full space-y-8 bg-white/10 backdrop-blur-lg p-10 rounded-2xl shadow-2xl border border-white/20">
            <div>
                <div
                    class="mx-auto h-16 w-16 rounded-full flex items-center justify-center shadow-lg"
                    :class="isAdminLogin ? 'bg-linear-to-br from-judo-blue to-judo-blue-dark' : 'bg-linear-to-br from-green-500 to-green-700'"
                    aria-hidden="true"
                >
                    <span class="text-3xl">{{ isAdminLogin ? '🥋' : '👨‍👩‍👧‍👦' }}</span>
                </div>
                <h2 class="mt-6 text-center text-3xl font-extrabold text-white">
                    {{ isAdminLogin ? 'Espace Club' : 'Espace Famille' }}
                </h2>
                <p class="mt-2 text-center text-sm text-blue-200">
                    {{ isAdminLogin ? "Accédez à l'espace de gestion du club" : "Gérez les inscriptions de vos enfants" }}
                </p>
            </div>
            <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
                <div class="rounded-md shadow-sm -space-y-px">
                    <div>
                        <label for="username" class="sr-only">Identifiant</label>
                        <input id="username" name="username" type="text" required v-model="username"
                            class="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-judo-blue focus:border-judo-blue focus:z-10 sm:text-sm bg-white/90 focus:bg-white transition"
                            placeholder="Identifiant">
                    </div>
                    <div>
                        <label for="password" class="sr-only">Mot de passe</label>
                        <input id="password" name="password" type="password" required v-model="password"
                            class="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-judo-blue focus:border-judo-blue focus:z-10 sm:text-sm bg-white/90 focus:bg-white transition"
                            placeholder="Mot de passe">
                    </div>
                </div>

                <div>
                    <button type="submit" :disabled="loading"
                        class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-judo-red hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-judo-red transition duration-300 transform hover:scale-105 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed">
                        <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                            <svg v-if="!loading" class="h-5 w-5 text-red-300 group-hover:text-red-200"
                                xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                                aria-hidden="true">
                                <path fill-rule="evenodd"
                                    d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                                    clip-rule="evenodd" />
                            </svg>
                            <svg v-else class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg"
                                fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                </path>
                            </svg>
                        </span>
                        {{ loading ? 'Connexion en cours...' : 'Se connecter' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/utils/axios'
import BaseButton from '../components/ui/BaseButton.vue'
import BaseInput from '../components/ui/BaseInput.vue'
import BaseCard from '../components/ui/BaseCard.vue'
import { useToastStore } from '../stores/toast'

const router = useRouter()
const toast = useToastStore()
const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)

const handleSignup = async () => {
    loading.value = true

    try {
        // Inscription de l'utilisateur
        const response = await api.post('/api/register/', {
            username: username.value,
            email: email.value,
            password: password.value
        })

        // Connexion automatique avec les tokens reçus
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        localStorage.setItem('username', username.value)

        toast.success("Compte créé avec succès !")
        router.push('/inscription')

    } catch (err) {
        console.error(err)
        toast.error("Erreur lors de l'inscription. Vérifiez les informations.")
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
                <div
                    class="mx-auto h-20 w-20 rounded-2xl flex items-center justify-center shadow-xl mb-6 bg-linear-to-br from-indigo-500 to-purple-600 transform transition-transform hover:scale-110">
                    <span class="text-4xl filter drop-shadow-md">🥋</span>
                </div>
                <h2 class="text-3xl font-extrabold text-white tracking-tight">
                    Créer un compte
                </h2>
                <p class="mt-2 text-blue-100 font-light">
                    Rejoignez l'espace parents du JCH
                </p>
            </div>

            <div class="px-8 pb-10">
                <form class="space-y-6" @submit.prevent="handleSignup">
                    <div class="space-y-4">
                        <BaseInput id="username" label="Nom d'utilisateur" v-model="username" required
                            placeholder="Votre identifiant" variant="glass">
                            <template #prefix>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-200" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                            </template>
                        </BaseInput>

                        <BaseInput id="email" label="Email" type="email" v-model="email" required
                            placeholder="votre@email.com" variant="glass">
                            <template #prefix>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-200" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                </svg>
                            </template>
                        </BaseInput>

                        <BaseInput id="password" label="Mot de passe" type="password" v-model="password" required
                            placeholder="••••••••" variant="glass">
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
                        <BaseButton type="submit" variant="primary" block :loading="loading" size="lg"
                            class="w-full bg-linear-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 shadow-lg hover:shadow-blue-500/50 border-none h-12 text-lg font-semibold">
                            S'inscrire
                        </BaseButton>
                    </div>
                </form>
            </div>

            <div class="px-8 py-4 bg-black/20 text-center rounded-b-2xl border-t border-white/5">
                <p class="text-sm text-blue-200">
                    Déjà un compte ?
                    <router-link to="/login"
                        class="font-bold text-white hover:text-blue-300 underline decoration-blue-400 decoration-2 underline-offset-4">
                        Se connecter
                    </router-link>
                </p>
            </div>
        </BaseCard>
    </div>
</template>

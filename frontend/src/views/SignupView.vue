<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/utils/axios'
import BaseButton from '../components/ui/BaseButton.vue'
import BaseInput from '../components/ui/BaseInput.vue'
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
    <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8 glass p-10 rounded-2xl">
            <div>
                <div class="mx-auto h-16 w-16 bg-white rounded-full flex items-center justify-center shadow-lg">
                    <span class="text-3xl">🥋</span>
                </div>
                <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
                    Créer un compte
                </h2>
                <p class="mt-2 text-center text-sm text-gray-600">
                    Rejoignez l'espace parents du JCH
                </p>
            </div>
            <form class="mt-8 space-y-6" @submit.prevent="handleSignup">
                <div class="space-y-4">
                    <BaseInput id="username" label="Nom d'utilisateur" v-model="username" required
                        placeholder="Votre identifiant" />
                    <BaseInput id="email" label="Email" type="email" v-model="email" required
                        placeholder="votre@email.com" />
                    <BaseInput id="password" label="Mot de passe" type="password" v-model="password" required
                        placeholder="••••••••" />
                </div>

                <div>
                    <BaseButton type="submit" variant="primary" block :loading="loading" size="lg">
                        S'inscrire
                    </BaseButton>
                </div>

                <div class="text-center mt-4">
                    <router-link to="/login" class="text-sm font-medium text-judo-blue hover:text-judo-blue-dark">
                        Déjà un compte ? Se connecter
                    </router-link>
                </div>
            </form>
        </div>
    </div>
</template>

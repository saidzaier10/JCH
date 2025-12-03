<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import api from '@/utils/axios'
import { useRouter } from 'vue-router'
import BaseButton from '../components/ui/BaseButton.vue'
import BaseInput from '../components/ui/BaseInput.vue'
import BaseCard from '../components/ui/BaseCard.vue'
import { useToastStore } from '../stores/toast'
import { useSeo } from '../composables/useSeo'

import { getWeightCategories } from '@/utils/judo-weights'

const router = useRouter()
useSeo('Inscription', 'Inscrivez-vous ou vos enfants au Judo Club Hem pour la nouvelle saison.')
const toast = useToastStore()
const season = ref(null)
const categories = ref([])
const existingChildren = ref([])
const loading = ref(true)
const submitting = ref(false)
const selectedChildId = ref(null)
const showAllCategories = ref(false)

// Stepper State
const currentStep = ref(1)
const steps = [
    { number: 1, title: 'Enfant' },
    { number: 2, title: 'Détails' },
    { number: 3, title: 'Catégorie' },
    { number: 4, title: 'Confirmation' }
]

const isAuthenticated = computed(() => !!localStorage.getItem('access_token'))

const form = ref({
    first_name: '',
    last_name: '',
    birth_date: '',
    gender: 'M',
    address: '',
    has_passport: false,
    category_id: null,
    weight_category: ''
})

const availableWeights = computed(() => {
    return getWeightCategories(form.value.birth_date, form.value.gender)
})

const fetchSeasonAndCategories = async () => {
    try {
        const seasonRes = await api.get('/api/seasons/active/')
        season.value = seasonRes.data

        const categoriesRes = await api.get('/api/categories/')
        categories.value = categoriesRes.data
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors du chargement des données.")
    }
}

const fetchChildren = async () => {
    if (!isAuthenticated.value) return
    try {
        const token = localStorage.getItem('access_token')
        const res = await api.get('/api/members/')
        existingChildren.value = res.data
    } catch (e) {
        console.error("Failed to fetch children", e)
    }
}

const selectChild = (child) => {
    selectedChildId.value = child.id
    form.value = {
        ...form.value,
        first_name: child.first_name,
        last_name: child.last_name,
        birth_date: child.birth_date,
        gender: child.gender,
        address: child.address,
        has_passport: child.has_passport,
        weight_category: child.weight_category || ''
    }
    nextStep()
}

const resetForm = () => {
    selectedChildId.value = null
    form.value = {
        first_name: '',
        last_name: '',
        birth_date: '',
        gender: 'M',
        address: '',
        has_passport: false,
        category_id: null,
        weight_category: ''
    }
    currentStep.value = 1
}

const filteredCategories = computed(() => {
    if (!form.value.birth_date || !season.value) return []

    const birthYear = new Date(form.value.birth_date).getFullYear()
    const seasonStartYear = new Date(season.value.start_date).getFullYear()
    const age = seasonStartYear - birthYear

    console.log('Debug Age:', { birthYear, seasonStartYear, age })
    console.log('Categories:', categories.value)

    return categories.value.filter(cat => {
        const min = cat.age_min !== null ? cat.age_min : 0
        const max = cat.age_max !== null ? cat.age_max : 999
        return age >= min && age <= max
    })
})

const displayedCategories = computed(() => {
    return showAllCategories.value ? categories.value : filteredCategories.value
})

const calculatedAge = computed(() => {
    if (!form.value.birth_date || !season.value) return null
    const birthYear = new Date(form.value.birth_date).getFullYear()
    const seasonStartYear = new Date(season.value.start_date).getFullYear()
    return seasonStartYear - birthYear
})

watch(filteredCategories, (newCats) => {
    if (newCats.length === 1) {
        form.value.category_id = newCats[0].id
    } else if (newCats.length === 0) {
        form.value.category_id = null
    } else {
        // If multiple, check if current selection is still valid
        if (form.value.category_id && !newCats.find(c => c.id === form.value.category_id)) {
            form.value.category_id = null
        }
    }
})

const nextStep = () => {
    if (currentStep.value === 1 && !selectedChildId.value && (!form.value.first_name || !form.value.last_name)) {
        // Allow creating new child, just check basic fields if manual entry
        // Actually step 1 is selection or new. If new, we go to step 2 to fill details.
    }
    currentStep.value++
}

const prevStep = () => {
    currentStep.value--
}

const submitRegistration = async () => {
    if (!form.value.category_id) {
        toast.error("Veuillez sélectionner une catégorie.")
        return
    }

    submitting.value = true

    try {
        const token = localStorage.getItem('access_token')
        const headers = { Authorization: `Bearer ${token}` }

        let memberId = selectedChildId.value

        // 1. Créer le membre si c'est un nouvel enfant
        if (!memberId) {
            const memberRes = await api.post('/api/members/', {
                first_name: form.value.first_name,
                last_name: form.value.last_name,
                birth_date: form.value.birth_date,
                gender: form.value.gender,
                address: form.value.address,
                has_passport: form.value.has_passport,
                weight_category: form.value.weight_category,
                email: '' // Pas requis pour les enfants
            })
            memberId = memberRes.data.id
            await fetchChildren()
        }

        // 2. Créer l'inscription
        await api.post('/api/registrations/', {
            member_id: memberId,
            season_id: season.value.id,
            category_id: form.value.category_id
        })

        toast.success("Inscription réussie !")
        resetForm()
        router.push('/my-space')
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de l'inscription. Vérifiez que l'enfant n'est pas déjà inscrit.")
    } finally {
        submitting.value = false
    }
}

onMounted(async () => {
    await fetchSeasonAndCategories()
    await fetchChildren()
    loading.value = false
})
</script>

<template>
    <div class="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-4xl mx-auto">
            <div class="text-center mb-12">
                <h1 class="text-3xl font-extrabold text-gray-900 sm:text-4xl">
                    Inscription Saison {{ season?.name }}
                </h1>
                <p class="mt-4 text-lg text-gray-600">
                    Rejoignez le Judo Club Hem pour une nouvelle année sportive !
                </p>
            </div>

            <!-- Auth Check -->
            <div v-if="!isAuthenticated" class="glass p-8 rounded-xl text-center max-w-2xl mx-auto">
                <div class="mx-auto h-16 w-16 bg-judo-blue/10 rounded-full flex items-center justify-center mb-6"
                    aria-hidden="true">
                    <span class="text-3xl">🔒</span>
                </div>
                <h2 class="text-2xl font-bold text-gray-900 mb-4">Connexion requise</h2>
                <p class="text-gray-600 mb-8">Pour inscrire votre enfant, vous devez créer un compte parent ou vous
                    connecter.</p>
                <div class="flex justify-center space-x-4">
                    <BaseButton variant="primary" @click="$router.push('/login')">Se connecter</BaseButton>
                    <BaseButton variant="white" @click="$router.push('/signup')">Créer un compte</BaseButton>
                </div>
            </div>

            <div v-else-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-judo-blue"></div>
            </div>

            <div v-else-if="!season" class="text-center py-12 glass rounded-xl">
                <p class="text-xl text-gray-500">Aucune saison active pour le moment.</p>
            </div>

            <div v-else class="glass rounded-xl overflow-hidden shadow-xl">
                <!-- Stepper Header -->
                <div class="bg-gray-50 border-b border-gray-200 px-8 py-4">
                    <div class="flex items-center justify-between" role="list">
                        <div v-for="step in steps" :key="step.number" class="flex items-center" role="listitem">
                            <div class="flex items-center relative"
                                :aria-current="currentStep === step.number ? 'step' : undefined">
                                <div class="rounded-full transition duration-500 ease-in-out h-8 w-8 py-3 border-2 flex items-center justify-center"
                                    :class="currentStep >= step.number ? 'bg-judo-blue border-judo-blue text-white' : 'border-gray-300 text-gray-500'">
                                    <span class="sr-only">Étape {{ step.number }}: </span>
                                    {{ step.number }}
                                </div>
                                <div class="absolute top-0 -ml-10 text-center mt-10 w-32 text-xs font-medium uppercase"
                                    :class="currentStep >= step.number ? 'text-judo-blue' : 'text-gray-500'"
                                    aria-hidden="true">
                                    {{ step.title }}
                                </div>
                            </div>
                            <div v-if="step.number !== steps.length"
                                class="flex-auto border-t-2 transition duration-500 ease-in-out w-12 sm:w-24 mx-4"
                                :class="currentStep > step.number ? 'border-judo-blue' : 'border-gray-300'"
                                aria-hidden="true">
                            </div>
                        </div>
                    </div>
                </div>

                <div class="p-8 mt-4 relative min-h-[400px]">
                    <transition name="fade" mode="out-in">
                        <!-- Step 1: Child Selection -->
                        <div v-if="currentStep === 1" key="step1">
                            <h3 class="text-xl font-bold text-gray-900 mb-6">Qui souhaitez-vous inscrire ?</h3>

                            <div v-if="existingChildren.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                                <div v-for="child in existingChildren" :key="child.id"
                                    class="border-2 border-transparent hover:border-judo-blue rounded-xl p-4 cursor-pointer bg-gray-50 transition-all hover:shadow-md"
                                    @click="selectChild(child)">
                                    <div class="flex items-center">
                                        <div
                                            class="h-10 w-10 rounded-full bg-judo-blue text-white flex items-center justify-center font-bold text-lg">
                                            {{ child.first_name.charAt(0) }}
                                        </div>
                                        <div class="ml-4">
                                            <p class="font-bold text-gray-900">{{ child.first_name }} {{
                                                child.last_name }}
                                            </p>
                                            <p class="text-sm text-gray-500">Né(e) le {{ child.birth_date }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="text-center">
                                <p v-if="existingChildren.length > 0" class="text-gray-500 mb-4">- OU -</p>
                                <BaseButton variant="secondary" @click="resetForm(); nextStep()">
                                    Inscrire un nouvel enfant
                                </BaseButton>
                            </div>
                        </div>

                        <!-- Step 2: Child Details -->
                        <div v-else-if="currentStep === 2" key="step2">
                            <h3 class="text-xl font-bold text-gray-900 mb-6">Informations de l'enfant</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <BaseInput label="Prénom" v-model="form.first_name" :disabled="!!selectedChildId"
                                    required />
                                <BaseInput label="Nom" v-model="form.last_name" :disabled="!!selectedChildId"
                                    required />
                                <BaseInput label="Date de naissance" type="date" v-model="form.birth_date"
                                    :disabled="!!selectedChildId" required />

                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Genre</label>
                                    <select v-model="form.gender" :disabled="!!selectedChildId"
                                        class="block w-full rounded-md border-gray-300 focus:ring-judo-blue focus:border-judo-blue shadow-sm sm:text-sm py-2 px-3">
                                        <option value="M">Masculin</option>
                                        <option value="F">Féminin</option>
                                    </select>
                                </div>

                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Catégorie de poids
                                        (Optionnel)</label>
                                    <select v-model="form.weight_category"
                                        class="block w-full rounded-md border-gray-300 focus:ring-judo-blue focus:border-judo-blue shadow-sm sm:text-sm py-2 px-3">
                                        <option value="">Sélectionner...</option>
                                        <option v-for="weight in availableWeights" :key="weight.value"
                                            :value="weight.value">
                                            {{ weight.label }}
                                        </option>
                                    </select>
                                </div>

                                <div class="md:col-span-2">
                                    <BaseInput label="Adresse" v-model="form.address" :disabled="!!selectedChildId" />
                                </div>

                                <div class="md:col-span-2 flex items-center">
                                    <input id="passport" v-model="form.has_passport" :disabled="!!selectedChildId"
                                        type="checkbox"
                                        class="h-4 w-4 text-judo-blue focus:ring-judo-blue border-gray-300 rounded">
                                    <label for="passport" class="ml-2 block text-sm text-gray-900">
                                        Possède déjà un passeport de Judo
                                    </label>
                                </div>
                            </div>
                            <div class="flex justify-between mt-8">
                                <BaseButton variant="ghost" @click="prevStep">Retour</BaseButton>
                                <BaseButton variant="primary" @click="nextStep"
                                    :disabled="!form.first_name || !form.last_name || !form.birth_date">Suivant
                                </BaseButton>
                            </div>
                        </div>

                        <!-- Step 3: Category Selection -->
                        <div v-else-if="currentStep === 3" key="step3">
                            <h3 class="text-xl font-bold text-gray-900 mb-6">Choix de la catégorie</h3>

                            <div v-if="filteredCategories.length === 0 && !showAllCategories"
                                class="text-center py-8 text-red-500 bg-red-50 rounded-lg">
                                <p>Aucune catégorie disponible pour l'année de naissance renseignée.</p>
                                <p class="text-sm mt-2 text-gray-600">Age calculé : {{ calculatedAge }} ans (Saison {{
                                    season?.name }})</p>
                                <button @click="showAllCategories = true" class="mt-4 text-judo-blue underline text-sm">
                                    Afficher toutes les catégories (dérogation)
                                </button>
                            </div>

                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div v-for="category in displayedCategories" :key="category.id"
                                    class="border-2 rounded-xl p-4 cursor-pointer transition-all"
                                    :class="form.category_id === category.id ? 'border-judo-blue bg-blue-50' : 'border-gray-200 hover:border-blue-300'"
                                    @click="form.category_id = category.id">
                                    <div class="flex justify-between items-start">
                                        <div>
                                            <h4 class="font-bold text-gray-900">{{ category.name }}</h4>
                                            <p class="text-sm text-gray-500 mt-1">{{ category.description }}</p>
                                            <p class="text-xs text-gray-400 mt-1">Age : {{ category.age_min }} - {{
                                                category.age_max }} ans</p>
                                        </div>
                                        <span class="font-bold text-judo-blue">{{ category.price }} €</span>
                                    </div>
                                </div>
                            </div>

                            <div class="flex justify-between mt-8">
                                <BaseButton variant="ghost" @click="prevStep">Retour</BaseButton>
                                <BaseButton variant="primary" @click="nextStep" :disabled="!form.category_id">Suivant
                                </BaseButton>
                            </div>
                        </div>

                        <!-- Step 4: Confirmation -->
                        <div v-else-if="currentStep === 4" key="step4">
                            <h3 class="text-xl font-bold text-gray-900 mb-6">Récapitulatif</h3>

                            <div class="bg-gray-50 rounded-xl p-6 mb-6 space-y-4">
                                <div class="flex justify-between border-b border-gray-200 pb-2">
                                    <span class="text-gray-500">Enfant</span>
                                    <span class="font-medium">{{ form.first_name }} {{ form.last_name }}</span>
                                </div>
                                <div class="flex justify-between border-b border-gray-200 pb-2">
                                    <span class="text-gray-500">Né(e) le</span>
                                    <span class="font-medium">{{ form.birth_date }}</span>
                                </div>
                                <div class="flex justify-between border-b border-gray-200 pb-2">
                                    <span class="text-gray-500">Catégorie</span>
                                    <span class="font-medium">{{categories.find(c => c.id === form.category_id)?.name
                                    }}</span>
                                </div>
                                <div class="flex justify-between pt-2">
                                    <span class="text-gray-900 font-bold">Total à payer</span>
                                    <span class="font-bold text-judo-blue text-xl">{{categories.find(c => c.id ===
                                        form.category_id)?.price}} €</span>
                                </div>
                            </div>

                            <div class="flex justify-between mt-8">
                                <BaseButton variant="ghost" @click="prevStep">Retour</BaseButton>
                                <BaseButton variant="primary" @click="submitRegistration" :loading="submitting">
                                    Confirmer
                                    l'inscription</BaseButton>
                            </div>
                        </div>
                    </transition>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import api from '@/utils/axios'
import { useRouter } from 'vue-router'
import BaseButton from '../components/ui/BaseButton.vue'
import BaseInput from '../components/ui/BaseInput.vue'
import BaseSelect from '../components/ui/BaseSelect.vue'
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

// État du Stepper (Étapes d'inscription)
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
    weight_category: '',
    discipline: 'JUDO',
    belt: 'WHITE',
    image_rights: false,
    city_hall_aid: false,
    city_hall_aid_amount: 0,
    has_supplementary_discipline: false
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

const activeRegistrationsCount = ref(0)
const fetchActiveRegistrations = async () => {
    if (!isAuthenticated.value) return
    try {
        const res = await api.get(`/api/registrations/?season_id=${season.value?.id}&status=VALIDATED`)
        // Simple count logic - in real app, might need more filtering
        activeRegistrationsCount.value = res.data.count || res.data.length || 0
    } catch (e) {
        console.error("Failed to fetch registrations", e)
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
        weight_category: child.weight_category || '',
        discipline: child.discipline || 'JUDO',
        belt: child.belt || 'WHITE',
        image_rights: child.image_rights || false,
        city_hall_aid: false,
        city_hall_aid_amount: 0,
        has_supplementary_discipline: false
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
        weight_category: '',
        discipline: 'JUDO',
        belt: 'WHITE',
        image_rights: false,
        city_hall_aid: false,
        city_hall_aid_amount: 0,
        has_supplementary_discipline: false
    }
    currentStep.value = 1
}

const filteredCategories = computed(() => {
    // Si pas de date de naissance ou de saison active, pas de catégories
    if (!form.value.birth_date || !season.value) return []

    // Calcul de l'âge théorique pour la saison
    const birthYear = new Date(form.value.birth_date).getFullYear()
    const seasonStartYear = new Date(season.value.start_date).getFullYear()
    const age = seasonStartYear - birthYear

    // console.log('Debug Age:', { birthYear, seasonStartYear, age })

    // Filtrage des catégories selon l'âge min/max
    return categories.value.filter(cat => {
        const min = cat.age_min !== null ? cat.age_min : 0
        const max = cat.age_max !== null ? cat.age_max : 999
        return age >= min && age <= max
    })
})

const registrationPrice = computed(() => {
    // Calcul dynamique du prix total à afficher avant paiement
    const category = categories.value.find(c => c.id === form.value.category_id)
    if (!category) return 0

    // Constantes (frais fixes)
    const LICENSE_FEE = 46
    const FILE_FEE = 10
    const FIXED_FEES = LICENSE_FEE + FILE_FEE
    const SUPPLEMENTARY_FEE = 40

    let total = parseFloat(category.price) + FIXED_FEES

    // Supplément discipline
    if (form.value.has_supplementary_discipline) {
        total += SUPPLEMENTARY_FEE
    }

    // Réduction famille
    // Note: On suppose que cette inscription sera la (count + 1)ème
    const familyRank = activeRegistrationsCount.value + 1
    let discount = 0

    if (familyRank === 2) {
        discount = 20
    } else if (familyRank >= 3) {
        discount = 40
    }

    total = total - discount

    // Déduction Aide Mairie
    if (form.value.city_hall_aid && form.value.city_hall_aid_amount) {
        total = total - parseFloat(form.value.city_hall_aid_amount)
    }

    return Math.max(0, total) // Empêcher le négatif
})

const priceDetails = computed(() => {
    const category = categories.value.find(c => c.id === form.value.category_id)
    if (!category) return []

    const details = [
        { label: `Cotisation (${category.name})`, amount: parseFloat(category.price) },
        { label: 'Licence FFJDA', amount: 46 },
        { label: 'Frais de dossier', amount: 10 }
    ]

    if (form.value.has_supplementary_discipline) {
        details.push({ label: 'Discipline supplémentaire', amount: 40 })
    }

    const familyRank = activeRegistrationsCount.value + 1
    if (familyRank === 2) {
        details.push({ label: 'Réduction famille (2ème membre)', amount: -20 })
    } else if (familyRank >= 3) {
        details.push({ label: 'Réduction famille (3ème+ membre)', amount: -40 })
    }

    if (form.value.city_hall_aid && form.value.city_hall_aid_amount) {
        details.push({ label: 'Aide Mairie / Pass Sport', amount: -parseFloat(form.value.city_hall_aid_amount) })
    }

    return details
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
    // Validation basique avant de passer à l'étape suivante si nécessaire
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
                discipline: form.value.discipline,
                belt: form.value.belt,
                image_rights: form.value.image_rights,
                email: '' // Pas requis pour les enfants
            })
            memberId = memberRes.data.id
            await fetchChildren()
        }

        // 2. Créer l'inscription
        await api.post('/api/registrations/', {
            member_id: memberId,
            season_id: season.value.id,
            category_id: form.value.category_id,
            city_hall_aid: form.value.city_hall_aid,
            city_hall_aid_amount: form.value.city_hall_aid_amount,
            has_supplementary_discipline: form.value.has_supplementary_discipline
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
    await fetchActiveRegistrations()
    loading.value = false
})
</script>

<template>
    <div
        class="min-h-screen py-12 px-4 sm:px-6 lg:px-8 bg-linear-to-br from-gray-900 via-blue-900 to-judo-blue relative overflow-hidden text-white font-sans">

        <!-- Background Decorations -->
        <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
            <div class="absolute top-10 left-10 w-64 h-64 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
            <div
                class="absolute bottom-20 right-20 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-1000">
            </div>
        </div>

        <div class="max-w-4xl mx-auto relative z-10">
            <div class="text-center mb-12">
                <h1 class="text-4xl font-extrabold text-white sm:text-5xl tracking-tight drop-shadow-lg">
                    Inscription Saison {{ season?.name }}
                </h1>
                <p class="mt-4 text-xl text-blue-200">
                    Rejoignez l'élite du Judo Club Hem.
                </p>
            </div>

            <!-- Auth Check -->
            <BaseCard v-if="!isAuthenticated" variant="glass" class="p-8 text-center max-w-2xl mx-auto">
                <div class="mx-auto h-20 w-20 bg-white/10 rounded-full flex items-center justify-center mb-6 shadow-inner"
                    aria-hidden="true">
                    <span class="text-4xl">🔒</span>
                </div>
                <h2 class="text-2xl font-bold text-white mb-4">Connexion requise</h2>
                <p class="text-blue-100 mb-8 max-w-md mx-auto">Pour inscrire votre enfant, connectez-vous à votre espace
                    parent ou créez un compte en quelques secondes.</p>
                <div class="flex justify-center space-x-4">
                    <BaseButton variant="primary" @click="$router.push('/login')" size="lg" shadow>Se connecter
                    </BaseButton>
                    <BaseButton variant="ghost" class="text-white hover:bg-white/10" @click="$router.push('/signup')"
                        size="lg">Créer un compte</BaseButton>
                </div>
            </BaseCard>

            <div v-else-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-white"></div>
            </div>

            <BaseCard v-else-if="!season" variant="glass" class="text-center py-12">
                <p class="text-xl text-gray-300">Aucune saison active pour le moment.</p>
            </BaseCard>

            <BaseCard v-else variant="glass" class="overflow-hidden shadow-2xl border border-white/10">
                <!-- Modern Stepper -->
                <div class="bg-black/20 border-b border-white/5 px-4 py-6 sm:px-8">
                    <div class="flex items-center justify-between max-w-3xl mx-auto relative">
                        <!-- Progress Bar Background -->
                        <div class="absolute top-1/2 left-0 w-full h-1 bg-white/10 -translate-y-1/2 rounded-full z-0">
                        </div>

                        <!-- Dynamic Progress Bar -->
                        <div class="absolute top-1/2 left-0 h-1 bg-blue-500 -translate-y-1/2 rounded-full z-0 transition-all duration-500"
                            :style="{ width: `${((currentStep - 1) / (steps.length - 1)) * 100}%` }">
                        </div>

                        <div v-for="step in steps" :key="step.number"
                            class="relative z-10 flex flex-col items-center group cursor-default">
                            <div class="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold border-2 transition-all duration-300 shadow-lg"
                                :class="[
                                    currentStep >= step.number
                                        ? 'bg-blue-600 border-blue-500 text-white scale-110 shadow-blue-500/50'
                                        : 'bg-gray-800 border-gray-600 text-gray-400 group-hover:border-gray-500'
                                ]">
                                <span v-if="currentStep > step.number">✓</span>
                                <span v-else>{{ step.number }}</span>
                            </div>
                            <span
                                class="mt-2 text-xs font-medium uppercase tracking-wider transition-colors duration-300"
                                :class="currentStep >= step.number ? 'text-blue-200' : 'text-gray-500'">
                                {{ step.title }}
                            </span>
                        </div>
                    </div>
                </div>

                <div class="p-6 sm:p-10 min-h-[500px]">
                    <transition name="fade" mode="out-in">
                        <!-- Step 1: Child Selection -->
                        <div v-if="currentStep === 1" key="step1"
                            class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                            <h3 class="text-2xl font-bold text-white mb-6 text-center">Qui souhaitez-vous inscrire ?
                            </h3>

                            <div v-if="existingChildren.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div v-for="child in existingChildren" :key="child.id"
                                    class="relative group border border-white/10 rounded-2xl p-6 cursor-pointer bg-white/5 hover:bg-white/10 transition-all duration-300 hover:shadow-xl hover:scale-105 hover:border-blue-500/50"
                                    @click="selectChild(child)">
                                    <div class="flex items-center space-x-4">
                                        <div
                                            class="h-14 w-14 rounded-full bg-linear-to-br from-blue-500 to-indigo-600 text-white flex items-center justify-center font-bold text-xl shadow-lg group-hover:shadow-blue-500/50 transition-shadow">
                                            {{ child.first_name.charAt(0) }}
                                        </div>
                                        <div>
                                            <p
                                                class="font-bold text-white text-lg group-hover:text-blue-200 transition-colors">
                                                {{ child.first_name }} {{ child.last_name }}</p>
                                            <p class="text-sm text-gray-400">Né(e) le {{ child.birth_date }}</p>
                                        </div>
                                        <div
                                            class="absolute right-4 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity text-blue-400">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none"
                                                viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M9 5l7 7-7 7" />
                                            </svg>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="text-center pt-4">
                                <p v-if="existingChildren.length > 0"
                                    class="text-gray-400 mb-6 font-medium text-sm uppercase tracking-widest">- OU -</p>
                                <button @click="resetForm(); nextStep()"
                                    class="group inline-flex items-center px-6 py-3 border border-white/30 text-base font-medium rounded-xl text-white bg-transparent hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200">
                                    <span class="mr-2 text-xl">+</span> Inscrire un nouvel enfant
                                </button>
                            </div>
                        </div>

                        <!-- Step 2: Child Details -->
                        <div v-else-if="currentStep === 2" key="step2"
                            class="animate-in fade-in slide-in-from-bottom-4 duration-500">
                            <h3 class="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">Informations de
                                l'enfant</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
                                <BaseInput label="Prénom" v-model="form.first_name" :disabled="!!selectedChildId"
                                    required variant="glass" placeholder="Ex: Thomas" />
                                <BaseInput label="Nom" v-model="form.last_name" :disabled="!!selectedChildId" required
                                    variant="glass" placeholder="Ex: Dupont" />
                                <BaseInput label="Date de naissance" type="date" v-model="form.birth_date"
                                    :disabled="!!selectedChildId" required variant="glass" />

                                <BaseSelect label="Genre" v-model="form.gender" :disabled="!!selectedChildId"
                                    variant="glass">
                                    <option value="M" class="text-gray-900">Masculin</option>
                                    <option value="F" class="text-gray-900">Féminin</option>
                                </BaseSelect>

                                <BaseSelect label="Discipline" v-model="form.discipline" :disabled="!!selectedChildId"
                                    variant="glass">
                                    <option value="EVEIL" class="text-gray-900">Judo Éveil</option>
                                    <option value="JUDO" class="text-gray-900">Judo</option>
                                    <option value="TAISO" class="text-gray-900">Taïso</option>
                                    <option value="TAISO_SENIOR" class="text-gray-900">Taïso Senior</option>
                                    <option value="APA" class="text-gray-900">Activité Physique Adaptée</option>
                                    <option value="JUJITSU" class="text-gray-900">Ju-Jitsu</option>
                                </BaseSelect>

                                <BaseSelect label="Ceinture Actuelle" v-model="form.belt" :disabled="!!selectedChildId"
                                    variant="glass">
                                    <option value="WHITE" class="text-gray-900">Blanche</option>
                                    <option value="WHITE_YELLOW" class="text-gray-900">Blanche-Jaune</option>
                                    <option value="YELLOW" class="text-gray-900">Jaune</option>
                                    <option value="YELLOW_ORANGE" class="text-gray-900">Jaune-Orange</option>
                                    <option value="ORANGE" class="text-gray-900">Orange</option>
                                    <option value="ORANGE_GREEN" class="text-gray-900">Orange-Verte</option>
                                    <option value="GREEN" class="text-gray-900">Verte</option>
                                    <option value="BLUE" class="text-gray-900">Bleue</option>
                                    <option value="BROWN" class="text-gray-900">Marron</option>
                                    <option value="BLACK" class="text-gray-900">Noire</option>
                                </BaseSelect>

                                <BaseSelect label="Catégorie de poids (Optionnel)" v-model="form.weight_category"
                                    variant="glass">
                                    <option value="" class="text-gray-900">Sélectionner...</option>
                                    <option v-for="weight in availableWeights" :key="weight.value" :value="weight.value"
                                        class="text-gray-900">
                                        {{ weight.label }}
                                    </option>
                                </BaseSelect>

                                <div class="md:col-span-2">
                                    <BaseInput label="Adresse" v-model="form.address" :disabled="!!selectedChildId"
                                        variant="glass" placeholder="Adresse complète" />
                                </div>

                                <!-- Checkboxes -->
                                <div class="md:col-span-2 space-y-4 pt-4">
                                    <label
                                        class="flex items-center p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors cursor-pointer group">
                                        <input type="checkbox" v-model="form.has_passport" :disabled="!!selectedChildId"
                                            class="w-5 h-5 text-blue-500 rounded border-white/30 bg-white/10 focus:ring-blue-500 focus:ring-offset-gray-900">
                                        <span
                                            class="ml-3 text-gray-200 group-hover:text-white transition-colors">Possède
                                            déjà un passeport de Judo</span>
                                    </label>

                                    <div class="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20">
                                        <label class="flex items-start cursor-pointer">
                                            <div class="flex items-center h-6">
                                                <input type="checkbox" v-model="form.image_rights"
                                                    :disabled="!!selectedChildId"
                                                    class="w-5 h-5 text-blue-500 rounded border-white/30 bg-white/10 focus:ring-blue-500 focus:ring-offset-gray-900">
                                            </div>
                                            <div class="ml-3 text-sm">
                                                <span class="font-medium text-blue-200">Droit à l'image</span>
                                                <p class="text-gray-400 mt-1 leading-relaxed text-xs">J'autorise le Judo
                                                    Club Hem à utiliser mon image ou celle de mon enfant (photos/vidéos
                                                    prises lors des cours ou événements) pour sa communication interne
                                                    et externe.</p>
                                            </div>
                                        </label>
                                    </div>
                                </div>
                            </div>

                            <div class="flex justify-between mt-10 pt-6 border-t border-white/10">
                                <BaseButton variant="ghost" class="text-gray-400 hover:text-white hover:bg-white/10"
                                    @click="prevStep">Retour</BaseButton>
                                <BaseButton variant="primary" @click="nextStep"
                                    :disabled="!form.first_name || !form.last_name || !form.birth_date">Suivant
                                </BaseButton>
                            </div>
                        </div>

                        <!-- Step 3: Category Selection -->
                        <div v-else-if="currentStep === 3" key="step3"
                            class="animate-in fade-in slide-in-from-bottom-4 duration-500">
                            <h3 class="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">Choix de la
                                catégorie</h3>

                            <div v-if="filteredCategories.length === 0 && !showAllCategories"
                                class="text-center py-10 bg-red-500/10 rounded-2xl border border-red-500/20">
                                <p class="text-red-300 font-medium">Aucune catégorie disponible pour l'âge calculé.</p>
                                <p class="text-sm mt-2 text-red-200/70">Age : {{ calculatedAge }} ans</p>
                                <button @click="showAllCategories = true"
                                    class="mt-4 text-white underline text-sm hover:text-red-200">
                                    Afficher toutes les catégories (dérogation)
                                </button>
                            </div>

                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div v-for="category in displayedCategories" :key="category.id"
                                    class="relative border-2 rounded-2xl p-6 cursor-pointer transition-all duration-300 flex flex-col justify-between"
                                    :class="form.category_id === category.id
                                        ? 'border-blue-500 bg-blue-500/20 shadow-lg shadow-blue-500/20'
                                        : 'border-white/10 bg-white/5 hover:bg-white/10 hover:border-white/20'"
                                    @click="form.category_id = category.id">

                                    <div class="absolute top-4 right-4" v-if="form.category_id === category.id">
                                        <div class="bg-blue-500 rounded-full p-1">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white"
                                                viewBox="0 0 20 20" fill="currentColor">
                                                <path fill-rule="evenodd"
                                                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                        </div>
                                    </div>

                                    <div>
                                        <h4 class="font-bold text-xl text-white mb-2">{{ category.name }}</h4>
                                        <p class="text-sm text-blue-200/80 mb-3">{{ category.description }}</p>
                                        <span
                                            class="inline-block px-3 py-1 bg-white/10 rounded-full text-xs text-gray-300">
                                            {{ category.age_min }} - {{ category.age_max }} ans
                                        </span>
                                    </div>
                                    <div class="mt-6 text-right">
                                        <span class="block text-2xl font-bold text-white">{{ category.price }} €</span>
                                        <span class="text-xs text-gray-500">+ Licence & Dossier</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Options Extras -->
                            <div class="mt-8 space-y-4">
                                <label
                                    class="flex items-center p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors cursor-pointer w-full">
                                    <input type="checkbox" v-model="form.has_supplementary_discipline"
                                        class="w-5 h-5 text-blue-500 rounded border-white/30 bg-white/10 focus:ring-blue-500 focus:ring-offset-gray-900">
                                    <span class="ml-3 font-medium text-gray-200">Discipline supplémentaire (+40€)</span>
                                </label>

                                <div class="p-4 rounded-xl bg-white/5 border border-white/10">
                                    <label class="flex items-center cursor-pointer mb-3">
                                        <input type="checkbox" v-model="form.city_hall_aid"
                                            class="w-5 h-5 text-blue-500 rounded border-white/30 bg-white/10 focus:ring-blue-500 focus:ring-offset-gray-900">
                                        <span class="ml-3 font-medium text-gray-200">Bénéficiaire d'une aide (Mairie /
                                            Pass'Sport) ?</span>
                                    </label>

                                    <div v-if="form.city_hall_aid"
                                        class="pl-8 animate-in slide-in-from-top-2 duration-200">
                                        <BaseInput type="number" label="Montant de l'aide (€)"
                                            v-model="form.city_hall_aid_amount" variant="glass" placeholder="0"
                                            class="max-w-xs" />
                                    </div>
                                </div>
                            </div>


                            <div class="flex justify-between mt-10 pt-6 border-t border-white/10">
                                <BaseButton variant="ghost" class="text-gray-400 hover:text-white hover:bg-white/10"
                                    @click="prevStep">Retour</BaseButton>
                                <BaseButton variant="primary" @click="nextStep" :disabled="!form.category_id">Suivant
                                </BaseButton>
                            </div>
                        </div>

                        <!-- Step 4: Confirmation -->
                        <div v-else-if="currentStep === 4" key="step4"
                            class="animate-in fade-in slide-in-from-bottom-4 duration-500">
                            <h3 class="text-2xl font-bold text-white mb-8 border-b border-white/10 pb-4">Récapitulatif &
                                Paiement</h3>

                            <div class="bg-white/5 backdrop-blur-md rounded-2xl p-6 mb-8 border border-white/10">
                                <h4 class="font-bold text-blue-200 mb-6 uppercase tracking-wider text-sm">Détail du
                                    tarif</h4>
                                <div class="space-y-4">
                                    <div v-for="(line, index) in priceDetails" :key="index"
                                        class="flex justify-between items-center text-sm border-b border-white/5 pb-3 last:border-0 last:pb-0">
                                        <span class="text-gray-300">{{ line.label }}</span>
                                        <span
                                            :class="line.amount < 0 ? 'text-green-400 font-medium' : 'text-white font-medium'">
                                            {{ line.amount > 0 ? '' : '' }}{{ line.amount }} €
                                        </span>
                                    </div>
                                </div>
                                <div class="flex justify-between pt-6 mt-4 border-t border-white/10">
                                    <span class="text-white font-bold text-xl">Total à payer</span>
                                    <span
                                        class="font-extrabold text-transparent bg-clip-text bg-linear-to-r from-blue-400 to-indigo-400 text-3xl">{{
                                        registrationPrice }} €</span>
                                </div>
                            </div>

                            <div class="mb-8">
                                <label
                                    class="block text-sm font-medium text-gray-400 mb-3 uppercase tracking-wider">Facilités
                                    de paiement</label>
                                <div class="grid grid-cols-2 gap-4">
                                    <div class="border-2 rounded-xl p-4 text-center cursor-pointer transition-all hover:bg-white/5"
                                        :class="'border-blue-500 bg-blue-500/20'">
                                        <div class="font-bold text-white text-lg">Comptant</div>
                                        <div class="text-sm text-blue-200 opacity-80 mt-1">1 x {{ registrationPrice }} €
                                        </div>
                                    </div>
                                    <div
                                        class="border-2 border-dashed border-gray-600 rounded-xl p-4 text-center cursor-not-allowed opacity-50">
                                        <div class="font-bold text-gray-400">3 Fois</div>
                                        <div class="text-xs text-gray-600 mt-1">(Bientôt disponible)</div>
                                    </div>
                                </div>
                            </div>

                            <div class="flex justify-between mt-10 pt-6 border-t border-white/10">
                                <BaseButton variant="ghost" class="text-gray-400 hover:text-white hover:bg-white/10"
                                    @click="prevStep">Retour</BaseButton>
                                <BaseButton variant="primary" @click="submitRegistration" :loading="submitting"
                                    size="lg" shadow
                                    class="bg-linear-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700">
                                    Confirmer et Payer
                                </BaseButton>
                            </div>
                        </div>
                    </transition>
                </div>
            </BaseCard>
        </div>
    </div>
</template>

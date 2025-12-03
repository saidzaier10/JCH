<script setup>
import { Calendar, Users, Trophy, ArrowRight } from 'lucide-vue-next'
import FeatureCard from '../components/FeatureCard.vue'
import { useSeo } from '../composables/useSeo'

useSeo('Accueil', 'Bienvenue au Judo Club Hem. Cours de judo pour tous âges et niveaux, compétitions et stages.')

const features = [
  {
    icon: Users,
    title: "Cours Tous Niveaux",
    description: "Du débutant à la ceinture noire, nos professeurs certifiés vous accompagnent dans votre progression technique et mentale."
  },
  {
    icon: Calendar,
    title: "Événements & Stages",
    description: "Participez à nos compétitions, stages de perfectionnement et événements conviviaux tout au long de l'année."
  },
  {
    icon: Trophy,
    title: "Compétition",
    description: "Intégrez nos équipes de compétition et représentez le Judo Club Hem lors des tournois régionaux et nationaux."
  }
]
</script>

<template>
  <div class="space-y-0">
    <!-- Hero Section -->
    <section class="relative bg-judo-blue text-white py-32 overflow-hidden">
      <!-- Background Pattern (Abstract Tatami/Judo texture could go here) -->
      <div class="absolute inset-0 overflow-hidden bg-linear-to-r from-judo-blue/90 to-judo-blue-dark/95"></div>

      <div class="container mx-auto px-4 relative z-10">
        <div class="max-w-4xl">
          <div
            class="inline-block bg-judo-red text-white text-xs font-bold px-3 py-1 rounded-sm mb-6 uppercase tracking-widest">
            Club Affilié FFJDA
          </div>
          <h1 class="text-5xl md:text-7xl font-bold mb-6 leading-tight uppercase tracking-tight">
            L'Esprit du Judo <br />
            <span class="text-transparent bg-clip-text bg-linear-to-r from-white to-gray-300">à Hem</span>
          </h1>
          <p class="text-xl md:text-2xl text-blue-100 mb-10 leading-relaxed max-w-2xl border-l-4 border-judo-red pl-6">
            Plus qu'un sport, une école de vie. Rejoignez nous pour apprendre, progresser et partager les valeurs du
            code moral.
          </p>
          <div class="flex flex-wrap gap-4">
            <a href="#"
              class="bg-judo-red text-white px-8 py-4 rounded-sm font-bold text-lg hover:bg-red-700 transition shadow-lg transform hover:-translate-y-1">
              Rejoindre le Club
            </a>
            <RouterLink to="/events"
              class="bg-white text-judo-blue px-8 py-4 rounded-sm font-bold text-lg hover:bg-gray-100 transition shadow-lg flex items-center">
              Voir le Calendrier
              <ArrowRight class="ml-2 h-5 w-5" />
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Grid -->
    <section class="py-20 bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-3xl md:text-4xl font-bold text-judo-blue uppercase tracking-wide mb-4">Nos Activités</h2>
          <div class="w-24 h-1 bg-judo-red mx-auto"></div>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <FeatureCard v-for="(feature, index) in features" :key="index" :icon="feature.icon" :title="feature.title"
            :description="feature.description" />
        </div>
      </div>
    </section>
  </div>
</template>

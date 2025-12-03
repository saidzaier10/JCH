<script setup>
import { MapPin } from 'lucide-vue-next'
</script>

<template>
  <div class="container mx-auto px-4 py-12">
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-judo-blue uppercase tracking-wide mb-4">Contact & Accès</h1>
      <div class="w-24 h-1 bg-judo-red mx-auto"></div>
    </div>

    <div class="max-w-4xl mx-auto bg-white rounded-sm shadow-xl overflow-hidden border-t-4 border-judo-red">
      <div class="p-8 bg-judo-blue text-white text-center">
        <h2 class="text-2xl font-bold mb-4 flex items-center justify-center uppercase tracking-wider">
          <MapPin class="mr-2 h-6 w-6" />
          Notre Localisation
        </h2>
        <p class="text-blue-100">Retrouvez-nous sur les tatamis à Hem !</p>
      </div>

      <!-- Google Maps Embed -->
      <div class="w-full h-96 bg-gray-200">
        <iframe 
          width="100%" 
          height="100%" 
          style="border:0" 
          loading="lazy" 
          allowfullscreen
          referrerpolicy="no-referrer-when-downgrade"
          src="https://maps.google.com/maps?q=Judo+Club+Hem+59510+Hem&t=&z=15&ie=UTF8&iwloc=&output=embed">
        </iframe>
      </div>

      <div class="p-8 text-center bg-gray-50">
        <p class="text-gray-500 italic">
          Les coordonnées complètes (téléphone, email) seront disponibles prochainement.
        </p>
      </div>
    </div>
  </div>
</template>

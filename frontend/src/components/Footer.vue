<script setup>
</script>

<template>
  <footer class="bg-gray-900 text-white py-12 border-t border-gray-800">
    <div class="container mx-auto px-4">
      <div class="grid md:grid-cols-4 gap-8 mb-8">
        <div class="col-span-1 md:col-span-2">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-8 h-8 bg-judo-red rounded-full flex items-center justify-center text-white font-bold text-xs">
              JCH</div>
            <h3 class="text-xl font-bold uppercase tracking-wider">Judo Club Hem</h3>
          </div>
          <p class="text-gray-400 text-sm leading-relaxed max-w-md">
            Le Judo Club Hem est une association sportive dédiée à l'enseignement et à la pratique du Judo et du
            Ju-jitsu.
            Rejoignez-nous pour partager les valeurs de notre code moral : Politesse, Courage, Sincérité, Honneur,
            Modestie, Respect, Contrôle de soi, Amitié.
          </p>
        </div>
        <div>
          <h3 class="text-lg font-bold uppercase tracking-wider mb-4 text-gray-200">Liens Rapides</h3>
          <ul class="space-y-2 text-sm text-gray-400">
            <li>
              <RouterLink to="/club" class="hover:text-judo-red transition">Le Club</RouterLink>
            </li>
            <li>
              <RouterLink to="/inscription" class="hover:text-judo-red transition">Inscription</RouterLink>
            </li>
            <li>
              <RouterLink to="/events" class="hover:text-judo-red transition">Événements</RouterLink>
            </li>
            <li>
              <RouterLink to="/admin/login" class="hover:text-judo-red transition">Accès Dirigeants</RouterLink>
            </li>
            <li><a href="#" class="hover:text-judo-red transition">Mentions Légales</a></li>
          </ul>
        </div>
        <div>
          <h3 class="text-lg font-bold uppercase tracking-wider mb-4 text-gray-200">Contact</h3>
          <ul class="space-y-2 text-sm text-gray-400">
            <li class="flex items-start">
              <span class="mr-2">📍</span>
              <span>Dojo Municipal<br>Rue des Écoles, 59510 Hem</span>
            </li>
            <li class="flex items-center">
              <span class="mr-2">📧</span>
              <a href="mailto:contact@judoclubhem.fr" class="hover:text-judo-red transition">contact@judoclubhem.fr</a>
            </li>
          </ul>
        </div>
      </div>
      <div
        class="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center text-sm text-gray-500">
        <div>&copy; {{ new Date().getFullYear() }} Judo Club Hem. Tous droits réservés.</div>
        <div class="mt-4 md:mt-0 flex space-x-4">
          <a href="#" class="hover:text-white transition">Facebook</a>
          <a href="#" class="hover:text-white transition">Instagram</a>
        </div>
      </div>
    </div>
  </footer>
</template>

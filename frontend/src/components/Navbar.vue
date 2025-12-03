<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { Menu, X, LogOut, User } from 'lucide-vue-next'

const isMenuOpen = ref(false)
const isLoggedIn = ref(false)
const scrolled = ref(false)
const router = useRouter()

const links = [
  { name: 'Accueil', path: '/' },
  { name: 'Le Club', path: '/club' },
  { name: 'Inscription', path: '/inscription' },
  { name: 'Événements', path: '/events' },
  { name: 'Galerie', path: '/gallery' },
  { name: 'Contact', path: '/contact' },
]

const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem('access_token')
}

const handleScroll = () => {
  scrolled.value = window.scrollY > 20
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('username')
  isLoggedIn.value = false
  router.push('/')
}

onMounted(() => {
  checkLoginStatus()
  window.addEventListener('storage', checkLoginStatus)
  window.addEventListener('scroll', handleScroll)
  setInterval(checkLoginStatus, 1000)
})
</script>

<template>
  <nav class="fixed w-full z-50 transition-all duration-300"
    :class="[scrolled || $route.path !== '/' ? 'bg-judo-blue/90 backdrop-blur-md shadow-lg py-2' : 'bg-transparent py-4']">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center space-x-3 group" aria-label="Retour à l'accueil">
          <div class="bg-white p-1 rounded-full shadow-md transition-transform group-hover:scale-110">
            <div
              class="w-10 h-10 bg-judo-red rounded-full flex items-center justify-center text-white font-bold text-xs">
              JCH
            </div>
          </div>
          <span class="text-2xl font-bold tracking-wider uppercase text-white drop-shadow-md">
            Judo Club Hem
          </span>
        </RouterLink>

        <!-- Desktop Menu -->
        <div class="hidden md:flex items-center space-x-8 font-semibold uppercase text-sm tracking-wide text-white">
          <RouterLink v-for="link in links" :key="link.path" :to="link.path" active-class="text-judo-red after:w-full"
            class="relative py-2 hover:text-judo-red transition-colors duration-300 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-0 after:h-0.5 after:bg-judo-red after:transition-all after:duration-300 hover:after:w-full"
            :aria-current="$route.path === link.path ? 'page' : undefined">
            {{ link.name }}
          </RouterLink>

          <div v-if="isLoggedIn" class="flex items-center space-x-4 ml-4">
            <RouterLink to="/my-space" class="text-white hover:text-judo-red transition font-medium">
              Mon Espace
            </RouterLink>
            <RouterLink to="/dashboard" class="flex items-center hover:text-judo-red transition">
              <User class="h-4 w-4 mr-1" />
              Admin
            </RouterLink>
            <button @click="logout" class="flex items-center hover:text-judo-red transition">
              <LogOut class="h-4 w-4 mr-1" />
              Déconnexion
            </button>
          </div>
          <RouterLink v-else to="/login"
            class="bg-judo-red hover:bg-red-600 text-white px-6 py-2 rounded-full font-bold transition-all duration-300 transform hover:-translate-y-0.5 shadow-lg hover:shadow-red-500/30">
            Connexion
          </RouterLink>
          <RouterLink v-if="!isLoggedIn" to="/admin/login"
            class="text-xs text-blue-200 hover:text-white transition uppercase tracking-widest border border-blue-200/30 px-3 py-1 rounded-sm hover:bg-white/10 ml-4">
            Espace Club
          </RouterLink>
        </div>

        <!-- Mobile Menu Button -->
        <button @click="isMenuOpen = !isMenuOpen" class="md:hidden text-white focus:outline-none"
          :aria-label="isMenuOpen ? 'Fermer le menu' : 'Ouvrir le menu'" :aria-expanded="isMenuOpen">
          <Menu v-if="!isMenuOpen" class="h-8 w-8" />
          <X v-else class="h-8 w-8" />
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <Transition enter-active-class="transition duration-200 ease-out"
      enter-from-class="transform -translate-y-4 opacity-0" enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-in" leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform -translate-y-4 opacity-0">
      <div v-show="isMenuOpen"
        class="md:hidden bg-judo-blue/95 backdrop-blur-xl border-t border-white/10 absolute w-full">
        <div class="px-4 pt-2 pb-6 space-y-2">
          <RouterLink v-for="link in links" :key="link.path" :to="link.path"
            class="block py-3 px-4 text-white hover:bg-white/10 rounded-lg transition" @click="isMenuOpen = false">
            {{ link.name }}
          </RouterLink>
          <div v-if="isLoggedIn" class="border-t border-white/10 pt-2 mt-2">
            <RouterLink to="/my-space" class="block py-3 px-4 text-white hover:bg-white/10 rounded-lg transition"
              @click="isMenuOpen = false">
              Mon Espace
            </RouterLink>
            <RouterLink to="/dashboard" class="block py-3 px-4 text-white hover:bg-white/10 rounded-lg transition"
              @click="isMenuOpen = false">
              Admin
            </RouterLink>
            <button @click="logout"
              class="w-full text-left py-3 px-4 text-white hover:bg-white/10 rounded-lg transition">
              Déconnexion
            </button>
          </div>
          <RouterLink v-else to="/login"
            class="block py-3 px-4 bg-judo-red text-center text-white font-bold rounded-lg mt-4 shadow-lg"
            @click="isMenuOpen = false">
            Connexion
          </RouterLink>
          <RouterLink v-if="!isLoggedIn" to="/admin/login"
            class="block py-3 px-4 text-center text-blue-200 hover:text-white hover:bg-white/10 rounded-lg transition text-sm uppercase tracking-widest mt-2"
            @click="isMenuOpen = false">
            Espace Club
          </RouterLink>
        </div>
      </div>
    </Transition>
  </nav>
</template>

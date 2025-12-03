<script setup>
import { RouterView, useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import ToastContainer from './components/ToastContainer.vue'

const route = useRoute()

</script>

<template>
  <div class="flex flex-col min-h-screen bg-gray-50 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]">
    <Navbar />
    <ToastContainer />
    <main class="grow" :class="route.path === '/' ? 'pt-0' : 'pt-20'">
      <RouterView />
    </main>
    <Footer />
  </div>
</template>

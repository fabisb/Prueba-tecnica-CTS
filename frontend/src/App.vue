<template>

  <nav class="bg-pink-600 text-white shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo -->
        <div class="flex-shrink-0 flex items-center">
          <RouterLink to="/" class="text-xl font-bold text-white hover:text-pink-200">
            <img src="@/assets/logo.svg" alt="Logo CTS" class="h-8 w-auto" />
          </RouterLink>
        </div>

        <!-- Links Desktop -->
        <div class="hidden md:flex space-x-6 items-center">
          <RouterLink to="/" class="hover:text-pink-200 transition-colors"
            :class="{ 'text-pink-200 font-semibold': $route.path === '/' }">
            Inicio
          </RouterLink>
          <RouterLink to="/admin/login" class="hover:text-pink-200 transition-colors"
            :class="{ 'text-pink-200 font-semibold': $route.path.startsWith('/admin') }">
            Administración
          </RouterLink>
        </div>

        <!-- Botón móvil -->
        <div class="flex md:hidden items-center">
          <button @click="isOpen = !isOpen" class="focus:outline-none">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path v-if="!isOpen" stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Menú móvil -->
    <div v-if="isOpen" class="md:hidden bg-pink-500">
      <RouterLink to="/" class="block px-4 py-2 hover:bg-pink-400"
        :class="{ 'bg-pink-400 font-semibold': $route.path === '/' }" @click="isOpen = false">
        Inicio
      </RouterLink>
      <RouterLink to="/admin/login" class="block px-4 py-2 hover:bg-pink-400"
        :class="{ 'bg-pink-400 font-semibold': $route.path.startsWith('/admin') }" @click="isOpen = false">
        Administración
      </RouterLink>
    </div>
  </nav>
  <div class="app-background min-h-screen flex flex-col">

    <RouterView />
  </div>

</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const isOpen = ref(false)
const $route = useRoute()
</script>

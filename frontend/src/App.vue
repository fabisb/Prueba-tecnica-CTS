<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <RouterLink to="/">Home</RouterLink> |
    <RouterLink to="/admin">Admin</RouterLink>
    <RouterView />
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  </div>
</template>

<style scoped>

</style>

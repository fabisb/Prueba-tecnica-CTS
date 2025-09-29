<template>
    <div>
        <h1>Verificación de correo</h1>
        <p v-if="message">{{ message }}</p>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const message = ref('')
const route = useRoute()

onMounted(async () => {
    const token = route.params.token
    try {
        const res = await axios.get(`http://localhost:8000/verify-email/${token}/`)
        message.value = res.data.message
    } catch (err) {
        message.value = err.response?.data?.error || 'Error en la verificación'
    }
})
</script>

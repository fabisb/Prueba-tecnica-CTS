<template>
    <div class="max-w-md mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Verificación de correo</h1>

        <div v-if="!verified">
            <p v-if="message">{{ message }}</p>
            <form @submit.prevent="setPassword">
                <input v-model="password" type="password" placeholder="Nueva contraseña" required
                    class="border p-2 w-full mb-2" />
                <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded cursor-pointer">Activar
                    cuenta</button>
            </form>
        </div>

        <div v-else>
            <p class="text-green-600 font-semibold">{{ message }}</p>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const token = route.params.token
const message = ref('')
const verified = ref(false)
const password = ref('')

onMounted(async () => {
    try {
        const res = await axios.get(`http://localhost:8000/api/users/verify-email/${token}/`)
        message.value = res.data.message
    } catch (err) {
        message.value = err.response?.data?.error || 'Token inválido'
    }
})

const setPassword = async () => {
    try {
        const res = await axios.post(`http://localhost:8000/api/users/verify-email/${token}/`, { password: password.value })
        message.value = res.data.message
        verified.value = true
    } catch (err) {
        message.value = err.response?.data?.error || 'Error al activar la cuenta'
    }
}
</script>

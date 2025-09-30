<template>
    <div class="min-h-screen bg-gray-100 flex items-center justify-center p-6">
        <div class="bg-white shadow-lg rounded-lg p-8 w-full max-w-md">
            <h1 class="text-2xl font-bold text-gray-800 mb-6 text-center">Registro al sorteo</h1>

            <form @submit.prevent="register" class="flex flex-col gap-4">
                <input v-model="first_name" placeholder="Nombre" required
                    class="border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <input v-model="last_name" placeholder="Apellido" required
                    class="border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <input v-model="email" type="email" placeholder="Correo" required
                    class="border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                <input v-model="phone" placeholder="Teléfono" required
                    class="border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />

                <button type="submit"
                    class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 rounded transition cursor-pointer">
                    Registrarse
                </button>
            </form>

            <p v-if="message" class="mt-4 text-center font-medium" :class="{
                'text-green-600': !message.includes('ya'),
                'text-red-600': message.includes('ya')
            }">
                {{ message }}
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const first_name = ref('')
const last_name = ref('')
const email = ref('')
const phone = ref('')
const message = ref('')

const register = async () => {
    try {
        const res = await axios.post('http://localhost:8000/api/users/registrar/', {
            first_name: first_name.value,
            last_name: last_name.value,
            email: email.value,
            phone: phone.value
        })
        console.log("🚀 ~ register ~ res:", res)
        message.value = '¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.'
    } catch (err) {
        message.value = err.response?.data?.email || err.response?.data?.detail || 'Error al registrar'
        if (err.response?.data?.email?.[0] === 'user with this email already exists.') {
            message.value = 'Este correo ya está registrado.'
        }
    }
}
</script>

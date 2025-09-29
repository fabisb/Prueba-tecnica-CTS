<template>
    <div>
        <h1>Registro al sorteo</h1>
        <form @submit.prevent="register">
            <input v-model="first_name" placeholder="Nombre" required />
            <input v-model="last_name" placeholder="Apellido" required />
            <input v-model="email" type="email" placeholder="Correo" required />
            <input v-model="phone" placeholder="Teléfono" required />
            <input v-model="password" type="password" placeholder="Contraseña" required />
            <button type="submit">Registrarse</button>
        </form>
        <p v-if="message">{{ message }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const first_name = ref('')
const last_name = ref('')
const email = ref('')
const phone = ref('')
const password = ref('')
const message = ref('')

const register = async () => {
    try {
        await axios.post('http://localhost:8000/registrar/', {
            first_name: first_name.value,
            last_name: last_name.value,
            email: email.value,
            phone: phone.value,
            password: password.value
        })
        message.value = '¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.'
    } catch (err) {
        message.value = err.response?.data?.email || err.response?.data?.detail || 'Error al registrar'
    }
}
</script>

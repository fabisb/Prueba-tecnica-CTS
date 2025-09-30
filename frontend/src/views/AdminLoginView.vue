<template>
    <div class="flex items-center justify-center min-h-screen bg-pink-50">
        <div class="bg-white p-8 rounded-xl shadow-lg w-full max-w-md border border-pink-200">
            <h1 class="text-3xl font-bold text-center text-pink-600 mb-6">Login Administrador</h1>

            <form @submit.prevent="login" class="flex flex-col gap-4">
                <div>
                    <label class="block text-pink-500 mb-1 font-semibold">Usuario</label>
                    <input v-model="username" type="text"
                        class="w-full px-4 py-2 rounded border border-pink-300 focus:outline-none focus:ring-2 focus:ring-pink-400"
                        required />
                </div>
                <div>
                    <label class="block text-pink-500 mb-1 font-semibold">Contraseña</label>
                    <input v-model="password" type="password"
                        class="w-full px-4 py-2 rounded border border-pink-300 focus:outline-none focus:ring-2 focus:ring-pink-400"
                        required />
                </div>

                <button type="submit"
                    class="w-full bg-pink-600 hover:bg-pink-500 text-white font-bold py-2 rounded transition">
                    Ingresar
                </button>
            </form>

            <p v-if="errorMessage" class="mt-4 text-center text-red-500 font-medium">
                {{ errorMessage }}
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"

const username = ref("")
const password = ref("")
const errorMessage = ref("")
const router = useRouter()

// Token en memoria
let adminToken = ref("")

const login = async () => {
    errorMessage.value = ""
    try {
        const res = await axios.post("http://localhost:8000/api/users/admin/login/", {
            username: username.value,
            password: password.value
        })

        const token = res.data.token
        if (!token) throw new Error("No se recibió token")

        adminToken.value = token
        localStorage.setItem('adminToken', token)
        axios.defaults.headers.common['Authorization'] = `Token ${token}`
        router.push("/admin")
    } catch (err) {
        console.error(err)
        if (err.response?.status === 401) {
            errorMessage.value = "Credenciales inválidas"
        } else {
            errorMessage.value = "Error al conectar con el servidor"
        }
    }
}
</script>

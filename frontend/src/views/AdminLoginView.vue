<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-900">
        <div class="bg-gray-800 p-8 rounded-xl shadow-md w-full max-w-md">
            <h1 class="text-2xl font-bold text-center text-white mb-6">Admin Login</h1>
            <form @submit.prevent="login">
                <div class="mb-4">
                    <label class="block text-gray-300 mb-2">Usuario</label>
                    <input v-model="username" type="text"
                        class="w-full px-3 py-2 rounded bg-gray-700 text-white focus:outline-none" required />
                </div>
                <div class="mb-4">
                    <label class="block text-gray-300 mb-2">Contraseña</label>
                    <input v-model="password" type="password"
                        class="w-full px-3 py-2 rounded bg-gray-700 text-white focus:outline-none" required />
                </div>
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 text-white py-2 rounded">
                    Ingresar
                </button>
            </form>
            <p v-if="errorMessage" class="mt-4 text-red-400 text-center">
                {{ errorMessage }}
            </p>
        </div>
    </div>
</template>
<script setup>
import { ref, nextTick } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"

const username = ref("")
const password = ref("")
const errorMessage = ref("")
const router = useRouter()

// Token en memoria
let adminToken = ref("")

const login = async () => {
    try {
        const res = await axios.post(
            "http://localhost:8000/api/users/admin/login/",
            {
                username: username.value,
                password: password.value
            }
        )

        const token = res.data.token
        console.log("🚀 ~ login ~ token:", token)
        if (!token) throw new Error("No se recibió token")

        adminToken.value = token
        axios.defaults.headers.common['Authorization'] = `Token ${token}`

        const sessionRes = await axios.get("http://localhost:8000/api/users/admin/session/")
        console.log("🚀 ~ login ~ sessionRes:", sessionRes)
        console.log("🚀 ~ login ~ sessionRes.data.is_authenticated:", sessionRes.data.is_authenticated)
        if (sessionRes.data.is_authenticated == true) {
            await nextTick()
            router.push("/admin")
        } else {
            errorMessage.value = "Error al verificar sesión"
        }
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

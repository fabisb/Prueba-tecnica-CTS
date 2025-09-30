<template>
    <div class="min-h-screen bg-gray-100 p-6">
        <div class="max-w-5xl mx-auto bg-white shadow-lg rounded-lg p-6">
            <h1 class="text-2xl font-bold text-gray-800 mb-4">Panel Admin - Concursantes</h1>

            <div class="flex flex-wrap gap-4 mb-6">
                <button @click="fetchParticipants"
                    class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded transition cursor-pointer">
                    Refrescar lista
                </button>
                <button @click="drawWinner"
                    class="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded transition cursor-pointer">
                    Generar ganador
                </button>
                <!-- Filtro por verificado -->
                <select v-model="filterVerified" @change="applyFilters" class="border rounded px-3 py-2">
                    <option value="">Todos</option>
                    <option value="true">Verificados</option>
                    <option value="false">No verificados</option>
                </select>

                <!-- Búsqueda -->
                <input v-model="searchQuery" @input="applyFilters" placeholder="Buscar por nombre o email"
                    class="border rounded px-3 py-2 flex-1" />
            </div>

            <div v-if="winner" class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6 rounded shadow-md">
                <h2 class="font-bold text-xl mb-1">🎉 Ganador:</h2>
                <p class="text-gray-800 text-lg">{{ winner.first_name }} {{ winner.last_name }} — {{ winner.email }}</p>
            </div>

            <table v-if="participants.length" class="w-full table-auto border-collapse">
                <thead>
                    <tr class="bg-gray-200 text-gray-700">
                        <th class="py-2 px-4 border">Nombre</th>
                        <th class="py-2 px-4 border">Email</th>
                        <th class="py-2 px-4 border">Verificado</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="p in participants" :key="p.id"
                        :class="['transition', index % 2 === 0 ? 'bg-gray-50' : 'bg-white', 'hover:bg-gray-100']">
                        <td class="py-2 px-4 border">{{ p.first_name }} {{ p.last_name }}</td>
                        <td class="py-2 px-4 border">{{ p.email }}</td>
                        <td class="py-2 px-4 border">
                            <span
                                :class="p.is_verified ? 'text-green-600 font-semibold' : 'text-red-600 font-semibold'">
                                {{ p.is_verified ? 'Sí' : 'No' }}
                            </span>
                        </td>
                    </tr>
                </tbody>

            </table>

            <p v-else class="text-gray-500 mt-4">No hay concursantes aún.</p>
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const participants = ref([])        // lista filtrada que se muestra en la tabla
const participantsRaw = ref([])     // lista completa sin filtrar
const winner = ref(null)
const router = useRouter()

const filterVerified = ref('')
const searchQuery = ref('')

// Traer participantes del backend
const fetchParticipants = async () => {
    try {
        const res = await axios.get('http://localhost:8000/api/users/admin/participants/')
        participantsRaw.value = res.data
        applyFilters()
    } catch (err) {
        console.error(err)
        if (err.response?.status === 401) {
            alert('No autorizado. Por favor, inicia sesión nuevamente.')
            router.push('/admin/login')
        }
    }
}

const applyFilters = () => {
    let filtered = [...participantsRaw.value]

    if (filterVerified.value === 'true') filtered = filtered.filter(p => p.is_verified)
    if (filterVerified.value === 'false') filtered = filtered.filter(p => !p.is_verified)

    if (searchQuery.value) {
        const q = searchQuery.value.toLowerCase()
        filtered = filtered.filter(p =>
            p.first_name.toLowerCase().includes(q) ||
            p.last_name.toLowerCase().includes(q) ||
            p.email.toLowerCase().includes(q)
        )
    }

    participants.value = filtered
}

// Generar ganador
const drawWinner = async () => {
    try {
        const res = await axios.post('http://localhost:8000/api/users/admin/participants/draw_winner/')
        winner.value = res.data.winner
    } catch (err) {
        console.error(err)
    }
}

// Inicialmente traemos participantes
fetchParticipants()
</script>

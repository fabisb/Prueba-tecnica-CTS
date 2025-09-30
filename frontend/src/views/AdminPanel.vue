<template>
    <div>
        <h1>Panel Admin - Concursantes</h1>
        <button @click="fetchParticipants">Refrescar lista</button>
        <button @click="drawWinner">Generar ganador</button>
        <div v-if="winner">
            <h2>Ganador:</h2>
            <p>{{ winner.first_name }} {{ winner.last_name }} — {{ winner.email }}</p>
        </div>
        <table v-if="participants.length">
            <thead>
                <tr>
                    <th>Nombre</th>
                    <th>Email</th>
                    <th>Verificado</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="p in participants" :key="p.id">
                    <td>{{ p.first_name }} {{ p.last_name }}</td>
                    <td>{{ p.email }}</td>
                    <td>{{ p.is_verified ? 'Sí' : 'No' }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const participants = ref([])
const winner = ref(null)

const fetchParticipants = async () => {
    try {
        const res = await axios.get('http://localhost:8000/api/users/admin/participants/')
        console.log("🚀 ~ fetchParticipants ~ res:", res.data)
        participants.value = res.data
    } catch (err) {
        console.error(err)
    }
}

const drawWinner = async () => {
    try {
        const res = await axios.post('http://localhost:8000/api/users/admin/participants/draw_winner/')
        winner.value = res.data.winner
    } catch (err) {
        console.error(err)
    }
}

// initial fetch
fetchParticipants()
</script>

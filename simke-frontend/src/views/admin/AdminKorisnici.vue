<template>
  <AdminLayout>
    <h1 class="text-h5 mb-4">Korisnici</h1>

    <v-card>
      <v-data-table :headers="zaglavlja" :items="korisnici">
        <template v-slot:item.uloga="{ item }">
          <v-chip :color="item.uloga === 'admin' ? 'info' : 'success'" size="small">{{ item.uloga }}</v-chip>
        </template>
        <template v-slot:item.akcije="{ item }">
          <v-btn v-if="item.uloga !== 'admin'" icon="mdi-delete" size="small" variant="text" color="error" @click="izbrisi(item.id)"></v-btn>
        </template>
      </v-data-table>
    </v-card>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AdminLayout from '../../components/AdminLayout.vue'

const korisnici = ref([])

const zaglavlja = [
  { title: 'ID', key: 'id' },
  { title: 'Ime', key: 'ime' },
  { title: 'Prezime', key: 'prezime' },
  { title: 'Email', key: 'email' },
  { title: 'Uloga', key: 'uloga' },
  { title: 'Akcije', key: 'akcije', sortable: false }
]

async function dohvati() {
  const r = await axios.get('http://127.0.0.1:5000/api/korisnici')
  korisnici.value = r.data
}

async function izbrisi(id) {
  if (!confirm('Sigurno?')) return
  await axios.delete(`http://127.0.0.1:5000/api/korisnici/${id}`)
  dohvati()
}

onMounted(dohvati)
</script>

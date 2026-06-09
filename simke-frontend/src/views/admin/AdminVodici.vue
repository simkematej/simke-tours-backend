<template>
  <AdminLayout>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h5">Vodiči</h1>
      <v-btn color="primary" @click="openModal()">+ Dodaj vodiča</v-btn>
    </div>

    <v-card>
      <v-data-table :headers="zaglavlja" :items="vodici">
        <template v-slot:item.ocjena="{ item }">
          {{ item.ocjena }} ★
        </template>
        <template v-slot:item.akcije="{ item }">
          <v-btn icon="mdi-pencil" size="small" variant="text" @click="openModal(item)"></v-btn>
          <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="izbrisi(item.id)"></v-btn>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="modal" max-width="500">
      <v-card>
        <v-card-title>{{ forma.id ? 'Uredi vodiča' : 'Novi vodič' }}</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field v-model="forma.ime" label="Ime" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="forma.prezime" label="Prezime" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model.number="forma.ocjena" label="Ocjena" type="number" step="0.1" min="1" max="5" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="forma.jezici" label="Jezici" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="forma.slika_url" label="URL slike" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="forma.bio" label="Biografija" variant="outlined" rows="4"></v-textarea>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="modal=false">Odustani</v-btn>
          <v-btn color="primary" @click="spremi">Spremi</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import axios from 'axios'
import AdminLayout from '../../components/AdminLayout.vue'

const vodici = ref([])
const modal = ref(false)

const zaglavlja = [
  { title: 'Ime', key: 'ime' },
  { title: 'Prezime', key: 'prezime' },
  { title: 'Ocjena', key: 'ocjena' },
  { title: 'Jezici', key: 'jezici' },
  { title: 'Akcije', key: 'akcije', sortable: false }
]

const forma = reactive({ id: null, ime: '', prezime: '', bio: '', ocjena: 4.5, jezici: '', slika_url: '' })

async function dohvati() {
  const r = await axios.get('http://127.0.0.1:5000/api/vodici')
  vodici.value = r.data
}

function openModal(v = null) {
  if (v) Object.assign(forma, { id: v.id, ime: v.ime, prezime: v.prezime, bio: v.bio, ocjena: v.ocjena, jezici: v.jezici, slika_url: v.slika_url })
  else Object.assign(forma, { id: null, ime: '', prezime: '', bio: '', ocjena: 4.5, jezici: '', slika_url: '' })
  modal.value = true
}

async function spremi() {
  if (forma.id) await axios.put(`http://127.0.0.1:5000/api/vodici/${forma.id}`, forma)
  else await axios.post('http://127.0.0.1:5000/api/vodici', forma)
  modal.value = false
  dohvati()
}

async function izbrisi(id) {
  if (!confirm('Sigurno?')) return
  await axios.delete(`http://127.0.0.1:5000/api/vodici/${id}`)
  dohvati()
}

onMounted(dohvati)
</script>

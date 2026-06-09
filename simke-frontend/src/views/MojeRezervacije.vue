<template>
  <v-container class="mt-4">
    <h1 class="text-h5 mb-4">Moje rezervacije</h1>

    <v-progress-circular v-if="ucitavam" indeterminate color="primary"></v-progress-circular>

    <v-alert v-else-if="rezervacije.length === 0" type="info">
      Nemate rezervacija. <RouterLink to="/putovi">Pregledajte putove</RouterLink>
    </v-alert>

    <v-row v-else>
      <v-col v-for="r in rezervacije" :key="r.id" cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex justify-space-between">
            {{ r.put_naziv }}
            <v-chip :color="statusBoja(r.status)" size="small">{{ statusLabel(r.status) }}</v-chip>
          </v-card-title>
          <v-card-subtitle>{{ r.put_destinacija }}</v-card-subtitle>
          <v-card-text>
            <div>Broj osoba: {{ r.broj_osoba }}</div>
            <div>Ukupno: <strong class="text-primary">{{ r.ukupna_cijena }} €</strong></div>
            <div>Datum: {{ r.datum_rezervacije }}</div>
            <div v-if="r.napomena">Napomena: {{ r.napomena }}</div>
          </v-card-text>
          <v-card-actions>
            <v-btn variant="outlined" :to="`/putovi/${r.put_id}`" size="small">Vidi put</v-btn>
            <v-btn v-if="r.status === 'na_cekanju'" color="error" size="small" @click="otkaziRezervaciju(r.id)">Otkaži</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const rezervacije = ref([])
const ucitavam = ref(true)

async function dohvati() {
  const r = await axios.get(`http://127.0.0.1:5000/api/rezervacije?korisnik_id=${auth.korisnik.id}`)
  rezervacije.value = r.data
  ucitavam.value = false
}

async function otkaziRezervaciju(id) {
  if (!confirm('Otkazati rezervaciju?')) return
  await axios.put(`http://127.0.0.1:5000/api/rezervacije/${id}`, { status: 'otkazano' })
  dohvati()
}

function statusLabel(s) {
  return { na_cekanju: 'Na čekanju', potvrdjeno: 'Potvrđeno', otkazano: 'Otkazano' }[s] || s
}

function statusBoja(s) {
  return { na_cekanju: 'warning', potvrdjeno: 'success', otkazano: 'error' }[s] || 'info'
}

onMounted(dohvati)
</script>

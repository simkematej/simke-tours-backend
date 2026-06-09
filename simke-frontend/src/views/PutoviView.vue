<template>
  <v-container class="mt-4">
    <h1 class="text-h5 mb-4">Putovi</h1>

    <v-row class="mb-4">
      <v-col cols="12" md="4">
        <v-text-field v-model="pretraga" label="Pretraži" variant="outlined" density="compact" clearable @keyup.enter="dohvati"></v-text-field>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" @click="dohvati">Traži</v-btn>
        <v-btn class="ml-2" variant="outlined" @click="reset">Resetiraj</v-btn>
      </v-col>
    </v-row>

    <v-row v-if="ucitavam">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col v-for="put in putovi" :key="put.id" cols="12" md="4">
        <v-card>
          <v-img :src="put.slika_url || defaultImg" height="180" cover></v-img>
          <v-card-title>{{ put.naziv }}</v-card-title>
          <v-card-subtitle>{{ put.destinacija }}, {{ put.zemlja }}</v-card-subtitle>
          <v-card-text>
            <div>Trajanje: {{ put.trajanje_dana }} dana</div>
            <div>Max osoba: {{ put.max_osoba }}</div>
            <div v-if="put.datum_polaska">Polazak: {{ put.datum_polaska }}</div>
            <div v-if="put.vodic_ime_prezime">Vodič: {{ put.vodic_ime_prezime }} ({{ put.vodic_ocjena }}★)</div>
            <div class="text-h6 mt-2 text-primary">{{ put.cijena }} €</div>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" :to="`/putovi/${put.id}`">Rezerviraj</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4" justify="center" v-if="pages > 1">
      <v-col cols="auto">
        <v-pagination v-model="page" :length="pages" @update:model-value="dohvati"></v-pagination>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const putovi = ref([])
const ucitavam = ref(true)
const pretraga = ref('')
const page = ref(1)
const pages = ref(1)
const defaultImg = 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=400'

async function dohvati() {
  ucitavam.value = true
  try {
    const r = await axios.get('http://127.0.0.1:5000/api/putovi', {
      params: { page: page.value, per_page: 6, q: pretraga.value }
    })
    putovi.value = r.data.items
    pages.value = r.data.pages
  } catch (e) {
    console.error(e)
  } finally {
    ucitavam.value = false
  }
}

function reset() {
  pretraga.value = ''
  page.value = 1
  dohvati()
}

onMounted(dohvati)
</script>

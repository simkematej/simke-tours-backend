<template>
  <v-container class="mt-4">
    <v-row>
      <v-col cols="12">
        <h1 class="text-h5 mb-4">Dobrodošli u Simke Tours</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3">
        <v-card color="primary" variant="tonal">
          <v-card-text class="text-center">
            <div class="text-h4">{{ stat.ukupno_putova }}</div>
            <div>Putova</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card color="success" variant="tonal">
          <v-card-text class="text-center">
            <div class="text-h4">{{ stat.ukupno_vodica }}</div>
            <div>Vodiča</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card color="warning" variant="tonal">
          <v-card-text class="text-center">
            <div class="text-h4">{{ stat.ukupno_korisnika }}</div>
            <div>Turista</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card color="info" variant="tonal">
          <v-card-text class="text-center">
            <div class="text-h4">{{ stat.ukupno_rezervacija }}</div>
            <div>Rezervacija</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <h2 class="text-h6 mb-3">Dostupni putovi</h2>
      </v-col>
      <v-col v-for="put in putovi" :key="put.id" cols="12" md="4">
        <v-card>
          <v-img :src="put.slika_url || defaultImg" height="180" cover></v-img>
          <v-card-title>{{ put.naziv }}</v-card-title>
          <v-card-subtitle>{{ put.destinacija }}, {{ put.zemlja }}</v-card-subtitle>
          <v-card-text>
            <div>Trajanje: {{ put.trajanje_dana }} dana</div>
            <div>Cijena: <strong>{{ put.cijena }} €</strong></div>
            <div v-if="put.vodic_ime_prezime">Vodič: {{ put.vodic_ime_prezime }} ({{ put.vodic_ocjena }}★)</div>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" :to="`/putovi/${put.id}`">Detalji</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-2">
      <v-col>
        <v-btn color="primary" variant="outlined" to="/putovi">Svi putovi</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const putovi = ref([])
const stat = ref({ ukupno_putova: 0, ukupno_vodica: 0, ukupno_korisnika: 0, ukupno_rezervacija: 0 })
const defaultImg = 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=400'

onMounted(async () => {
  const r = await axios.get('http://127.0.0.1:5000/api/putovi?per_page=3')
  putovi.value = r.data.items
  const s = await axios.get('http://127.0.0.1:5000/api/statistike')
  stat.value = s.data
})
</script>

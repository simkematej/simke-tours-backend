<template>
  <v-container class="mt-4">
    <v-btn variant="text" to="/putovi" prepend-icon="mdi-arrow-left" class="mb-4">Nazad</v-btn>

    <v-row v-if="put">
      <v-col cols="12" md="8">
        <v-card>
          <v-img :src="put.slika_url || defaultImg" height="280" cover></v-img>
          <v-card-title class="text-h5">{{ put.naziv }}</v-card-title>
          <v-card-subtitle>{{ put.destinacija }}, {{ put.zemlja }}</v-card-subtitle>
          <v-card-text>
            <v-row>
              <v-col cols="6" md="3">
                <div class="text-caption">Trajanje</div>
                <div class="font-weight-bold">{{ put.trajanje_dana }} dana</div>
              </v-col>
              <v-col cols="6" md="3">
                <div class="text-caption">Polazak</div>
                <div class="font-weight-bold">{{ put.datum_polaska || 'Po dogovoru' }}</div>
              </v-col>
              <v-col cols="6" md="3">
                <div class="text-caption">Max osoba</div>
                <div class="font-weight-bold">{{ put.max_osoba }}</div>
              </v-col>
              <v-col cols="6" md="3">
                <div class="text-caption">Kategorija</div>
                <div class="font-weight-bold">{{ put.kategorija }}</div>
              </v-col>
            </v-row>
            <v-divider class="my-3"></v-divider>
            <p>{{ put.opis }}</p>
          </v-card-text>
        </v-card>

        <v-card class="mt-4" v-if="vodic">
          <v-card-title>Vodič</v-card-title>
          <v-card-text>
            <v-row align="center">
              <v-col cols="auto">
                <v-avatar size="60">
                  <v-img :src="vodic.slika_url || 'https://i.pravatar.cc/60'"></v-img>
                </v-avatar>
              </v-col>
              <v-col>
                <div class="font-weight-bold">{{ vodic.ime }} {{ vodic.prezime }}</div>
                <div>Ocjena: {{ vodic.ocjena }} ★</div>
                <div class="text-caption">{{ vodic.jezici }}</div>
              </v-col>
            </v-row>
            <p class="mt-3">{{ vodic.bio }}</p>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card>
          <v-card-title class="text-h5 text-primary">{{ put.cijena }} €</v-card-title>
          <v-card-subtitle>po osobi</v-card-subtitle>
          <v-card-text>
            <div v-if="!auth.jePrijavljenKorisnik">
              <p class="mb-3">Prijavi se za rezervaciju</p>
              <v-btn color="primary" to="/prijava" block class="mb-2">Prijavi se</v-btn>
              <v-btn variant="outlined" to="/registracija" block>Registriraj se</v-btn>
            </div>
            <div v-else>
              <v-alert v-if="uspjeh" type="success" class="mb-3">{{ uspjeh }}</v-alert>
              <v-alert v-if="greska" type="error" class="mb-3">{{ greska }}</v-alert>
              <v-select v-model="brojOsoba" :items="Array.from({length: put.max_osoba}, (_, i) => i+1)" label="Broj osoba" variant="outlined" class="mb-2"></v-select>
              <v-textarea v-model="napomena" label="Napomena" variant="outlined" rows="3" class="mb-2"></v-textarea>
              <div class="d-flex justify-space-between mb-3">
                <span>Ukupno:</span>
                <strong class="text-primary">{{ (put.cijena * brojOsoba).toFixed(2) }} €</strong>
              </div>
              <v-btn color="primary" @click="rezerviraj" block>Rezerviraj</v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth.js'

const route = useRoute()
const auth = useAuthStore()
const put = ref(null)
const vodic = ref(null)
const brojOsoba = ref(1)
const napomena = ref('')
const uspjeh = ref('')
const greska = ref('')
const defaultImg = 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=600'

onMounted(async () => {
  const r = await axios.get(`http://127.0.0.1:5000/api/putovi/${route.params.id}`)
  put.value = r.data
  if (r.data.vodic_id) {
    const rv = await axios.get(`http://127.0.0.1:5000/api/vodici/${r.data.vodic_id}`)
    vodic.value = rv.data
  }
})

async function rezerviraj() {
  uspjeh.value = ''
  greska.value = ''
  try {
    await axios.post('http://127.0.0.1:5000/api/rezervacije', {
      korisnik_id: auth.korisnik.id,
      put_id: put.value.id,
      broj_osoba: brojOsoba.value,
      napomena: napomena.value
    })
    uspjeh.value = 'Rezervacija je uspješno napravljena!'
    napomena.value = ''
  } catch (e) {
    greska.value = 'Greška pri rezervaciji'
  }
}
</script>

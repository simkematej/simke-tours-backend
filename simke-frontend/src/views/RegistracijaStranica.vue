<template>
  <v-container class="mt-8">
    <v-row justify="center">
      <v-col cols="12" md="5">
        <v-card>
          <v-card-title class="text-h6 pa-4">Registracija</v-card-title>
          <v-card-text>
            <v-alert v-if="greska" type="error" class="mb-3">{{ greska }}</v-alert>
            <v-text-field v-model="forma.ime" label="Ime" variant="outlined" class="mb-2"></v-text-field>
            <v-text-field v-model="forma.prezime" label="Prezime" variant="outlined" class="mb-2"></v-text-field>
            <v-text-field v-model="forma.email" label="Email" type="email" variant="outlined" class="mb-2"></v-text-field>
            <v-text-field v-model="forma.lozinka" label="Lozinka" type="password" variant="outlined"></v-text-field>
          </v-card-text>
          <v-card-actions class="pa-4">
            <v-btn color="primary" @click="registracija" block>Registriraj se</v-btn>
          </v-card-actions>
          <v-card-text class="text-center">
            Već imaš račun? <RouterLink to="/prijava">Prijavi se</RouterLink>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth.js'

const forma = reactive({ ime: '', prezime: '', email: '', lozinka: '' })
const greska = ref('')
const auth = useAuthStore()
const router = useRouter()

async function registracija() {
  greska.value = ''
  try {
    const r = await axios.post('http://127.0.0.1:5000/api/registracija', forma)
    auth.prijavi(r.data.korisnik)
    router.push('/putovi')
  } catch (e) {
    greska.value = e.response?.data?.greska || 'Greška pri registraciji'
  }
}
</script>

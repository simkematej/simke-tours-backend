<template>
  <v-container class="mt-8">
    <v-row justify="center">
      <v-col cols="12" md="5">
        <v-card>
          <v-card-title class="text-h6 pa-4">Prijava</v-card-title>
          <v-card-text>
            <v-alert v-if="greska" type="error" class="mb-3">{{ greska }}</v-alert>
            <v-text-field v-model="email" label="Email" type="email" variant="outlined" class="mb-2"></v-text-field>
            <v-text-field v-model="lozinka" label="Lozinka" type="password" variant="outlined" @keyup.enter="prijava"></v-text-field>

          </v-card-text>
          <v-card-actions class="pa-4">
            <v-btn color="primary" @click="prijava" block>Prijavi se</v-btn>
          </v-card-actions>
          <v-card-text class="text-center">
            Nemaš račun? <RouterLink to="/registracija">Registriraj se</RouterLink>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth.js'

const email = ref('')
const lozinka = ref('')
const greska = ref('')
const auth = useAuthStore()
const router = useRouter()

async function prijava() {
  greska.value = ''
  try {
    const r = await axios.post('http://127.0.0.1:5000/api/prijava', { email: email.value, lozinka: lozinka.value })
    auth.prijavi(r.data.korisnik)
    if (r.data.korisnik.uloga === 'admin') router.push('/admin')
    else router.push('/putovi')
  } catch (e) {
    greska.value = e.response?.data?.greska || 'Pogrešan email ili lozinka'
  }
}
</script>

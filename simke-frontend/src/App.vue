<template>
  <v-app>
    <v-app-bar color="primary" flat>
      <v-app-bar-title>
        <RouterLink to="/" style="color:white; text-decoration:none;">Simke Tours</RouterLink>
      </v-app-bar-title>
      <v-btn variant="text" color="white" to="/putovi">Putovi</v-btn>
      <template v-if="auth.jePrijavljenKorisnik">
        <v-btn v-if="!auth.jeAdminkorisnik" variant="text" color="white" to="/moje-rezervacije">Moje rezervacije</v-btn>
        <v-btn v-if="auth.jeAdminkorisnik" variant="text" color="white" to="/admin">Admin</v-btn>
        <v-btn variant="outlined" color="white" @click="odjava">Odjava</v-btn>
      </template>
      <template v-else>
        <v-btn variant="text" color="white" to="/prijava">Prijava</v-btn>
        <v-btn variant="outlined" color="white" to="/registracija">Registracija</v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth.js'

const auth = useAuthStore()
const router = useRouter()

function odjava() {
  auth.odjavi()
  router.push('/')
}
</script>

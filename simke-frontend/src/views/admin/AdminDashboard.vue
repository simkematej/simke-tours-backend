<template>
  <AdminLayout>
    <h1 class="text-h5 mb-4">Dashboard</h1>

    <v-row v-if="stat">
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
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Status rezervacija</v-card-title>
          <v-card-text>
            <div class="d-flex justify-space-between mb-2">
              <span>Na čekanju:</span>
              <v-chip color="warning" size="small">{{ stat?.na_cekanju }}</v-chip>
            </div>
            <div class="d-flex justify-space-between">
              <span>Potvrđene:</span>
              <v-chip color="success" size="small">{{ stat?.potvrdjene_rezervacije }}</v-chip>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Brze akcije</v-card-title>
          <v-card-actions>
            <v-btn color="primary" to="/admin/putovi">+ Novi put</v-btn>
            <v-btn variant="outlined" to="/admin/vodici">+ Novi vodič</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AdminLayout from '../../components/AdminLayout.vue'

const stat = ref(null)

onMounted(async () => {
  const r = await axios.get('http://127.0.0.1:5000/api/statistike')
  stat.value = r.data
})
</script>

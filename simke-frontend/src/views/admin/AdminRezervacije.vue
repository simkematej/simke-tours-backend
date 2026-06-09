<template>
  <AdminLayout>
    <h1 class="text-h5 mb-4">Rezervacije</h1>

    <v-card>
      <v-data-table :headers="zaglavlja" :items="rezervacije">
        <template v-slot:item.status="{ item }">
          <v-chip :color="statusBoja(item.status)" size="small">{{ statusLabel(item.status) }}</v-chip>
        </template>
        <template v-slot:item.ukupna_cijena="{ item }">
          {{ item.ukupna_cijena }} €
        </template>
        <template v-slot:item.akcije="{ item }">
          <v-select
            :model-value="item.status"
            :items="[{title:'Na čekanju',value:'na_cekanju'},{title:'Potvrdi',value:'potvrdjeno'},{title:'Otkaži',value:'otkazano'}]"
            variant="outlined"
            density="compact"
            hide-details
            style="min-width:130px"
            item-title="title"
            item-value="value"
            @update:model-value="promijeniStatus(item.id, $event)"
          ></v-select>
        </template>
      </v-data-table>
    </v-card>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AdminLayout from '../../components/AdminLayout.vue'

const rezervacije = ref([])

const zaglavlja = [
  { title: 'ID', key: 'id' },
  { title: 'Turist', key: 'korisnik_ime' },
  { title: 'Put', key: 'put_naziv' },
  { title: 'Osoba', key: 'broj_osoba' },
  { title: 'Ukupno', key: 'ukupna_cijena' },
  { title: 'Datum', key: 'datum_rezervacije' },
  { title: 'Status', key: 'status' },
  { title: 'Promijeni', key: 'akcije', sortable: false }
]

async function dohvati() {
  const r = await axios.get('http://127.0.0.1:5000/api/rezervacije')
  rezervacije.value = r.data
}

async function promijeniStatus(id, status) {
  await axios.put(`http://127.0.0.1:5000/api/rezervacije/${id}`, { status })
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

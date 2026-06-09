<template>
  <AdminLayout>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h5">Putovi</h1>
      <v-btn color="primary" @click="openModal()">+ Dodaj put</v-btn>
    </div>

    <v-card>
      <v-data-table :headers="zaglavlja" :items="putovi" :loading="ucitavam">
        <template v-slot:item.cijena="{ item }">
          {{ item.cijena }} €
        </template>
        <template v-slot:item.akcije="{ item }">
          <v-btn icon="mdi-pencil" size="small" variant="text" @click="openModal(item)"></v-btn>
          <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="izbrisi(item.id)"></v-btn>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="modal" max-width="600">
      <v-card>
        <v-card-title>{{ forma.id ? 'Uredi put' : 'Novi put' }}</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field v-model="forma.naziv" label="Naziv" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="forma.destinacija" label="Destinacija" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="forma.zemlja" label="Zemlja" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model.number="forma.cijena" label="Cijena (€)" type="number" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model.number="forma.trajanje_dana" label="Trajanje (dana)" type="number" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model.number="forma.max_osoba" label="Max osoba" type="number" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="forma.datum_polaska" label="Datum polaska" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-select v-model="forma.kategorija" :items="['kulturni','plažni','avantura']" label="Kategorija" variant="outlined" density="compact"></v-select>
            </v-col>
            <v-col cols="12" md="6">
              <v-select v-model="forma.vodic_id" :items="vodiciDropdown" label="Vodič" variant="outlined" density="compact" item-title="title" item-value="value"></v-select>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="forma.slika_url" label="URL slike" variant="outlined" density="compact"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="forma.opis" label="Opis" variant="outlined" rows="3"></v-textarea>
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
import { ref, onMounted, reactive, computed } from 'vue'
import axios from 'axios'
import AdminLayout from '../../components/AdminLayout.vue'

const putovi = ref([])
const vodici = ref([])
const modal = ref(false)
const ucitavam = ref(true)

const zaglavlja = [
  { title: 'Naziv', key: 'naziv' },
  { title: 'Destinacija', key: 'destinacija' },
  { title: 'Zemlja', key: 'zemlja' },
  { title: 'Cijena', key: 'cijena' },
  { title: 'Vodič', key: 'vodic_ime_prezime' },
  { title: 'Akcije', key: 'akcije', sortable: false }
]

const vodiciDropdown = computed(() => [
  { title: '-', value: '' },
  ...vodici.value.map(v => ({ title: `${v.ime} ${v.prezime}`, value: v.id }))
])

const forma = reactive({ id: null, naziv: '', destinacija: '', zemlja: '', opis: '', cijena: 999, trajanje_dana: 7, max_osoba: 12, datum_polaska: '', slika_url: '', kategorija: 'kulturni', vodic_id: '' })

async function dohvati() {
  ucitavam.value = true
  const r = await axios.get('http://127.0.0.1:5000/api/putovi?per_page=100')
  putovi.value = r.data.items
  ucitavam.value = false
}

async function dohvatiVodice() {
  const r = await axios.get('http://127.0.0.1:5000/api/vodici')
  vodici.value = r.data
}

function openModal(p = null) {
  if (p) Object.assign(forma, { id: p.id, naziv: p.naziv, destinacija: p.destinacija, zemlja: p.zemlja, opis: p.opis, cijena: p.cijena, trajanje_dana: p.trajanje_dana, max_osoba: p.max_osoba, datum_polaska: p.datum_polaska, slika_url: p.slika_url, kategorija: p.kategorija, vodic_id: p.vodic_id })
  else Object.assign(forma, { id: null, naziv: '', destinacija: '', zemlja: '', opis: '', cijena: 999, trajanje_dana: 7, max_osoba: 12, datum_polaska: '', slika_url: '', kategorija: 'kulturni', vodic_id: '' })
  modal.value = true
}

async function spremi() {
  if (forma.id) await axios.put(`http://127.0.0.1:5000/api/putovi/${forma.id}`, forma)
  else await axios.post('http://127.0.0.1:5000/api/putovi', forma)
  modal.value = false
  dohvati()
}

async function izbrisi(id) {
  if (!confirm('Sigurno?')) return
  await axios.delete(`http://127.0.0.1:5000/api/putovi/${id}`)
  dohvati()
}

onMounted(() => { dohvati(); dohvatiVodice() })
</script>

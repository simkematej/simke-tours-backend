import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const korisnik = ref(JSON.parse(localStorage.getItem('korisnik') || 'null'))

  const jeAdminkorisnik = computed(() => korisnik.value?.uloga === 'admin')
  const jePrijavljenKorisnik = computed(() => !!korisnik.value)

  function prijavi(k) {
    korisnik.value = k
    localStorage.setItem('korisnik', JSON.stringify(k))
  }

  function odjavi() {
    korisnik.value = null
    localStorage.removeItem('korisnik')
  }

  return { korisnik, jeAdminkorisnik, jePrijavljenKorisnik, prijavi, odjavi }
})

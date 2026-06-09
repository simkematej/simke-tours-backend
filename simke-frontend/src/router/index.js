import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

import PocetnaView from '../views/PocetnaView.vue'
import PrijavaStranica from '../views/PrijavaStranica.vue'
import RegistracijaStranica from '../views/RegistracijaStranica.vue'
import PutoviView from '../views/PutoviView.vue'
import PutDetalj from '../views/PutDetalj.vue'
import MojeRezervacije from '../views/MojeRezervacije.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminPutovi from '../views/admin/AdminPutovi.vue'
import AdminVodici from '../views/admin/AdminVodici.vue'
import AdminRezervacije from '../views/admin/AdminRezervacije.vue'
import AdminKorisnici from '../views/admin/AdminKorisnici.vue'

const routes = [
  { path: '/', component: PocetnaView },
  { path: '/prijava', component: PrijavaStranica },
  { path: '/registracija', component: RegistracijaStranica },
  { path: '/putovi', component: PutoviView },
  { path: '/putovi/:id', component: PutDetalj },
  {
    path: '/moje-rezervacije',
    component: MojeRezervacije,
    meta: { zahtijeva_prijavu: true }
  },
  {
    path: '/admin',
    component: AdminDashboard,
    meta: { zahtijeva_admin: true }
  },
  {
    path: '/admin/putovi',
    component: AdminPutovi,
    meta: { zahtijeva_admin: true }
  },
  {
    path: '/admin/vodici',
    component: AdminVodici,
    meta: { zahtijeva_admin: true }
  },
  {
    path: '/admin/rezervacije',
    component: AdminRezervacije,
    meta: { zahtijeva_admin: true }
  },
  {
    path: '/admin/korisnici',
    component: AdminKorisnici,
    meta: { zahtijeva_admin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.zahtijeva_admin && !auth.jeAdminkorisnik) {
    return '/prijava'
  }
  if (to.meta.zahtijeva_prijavu && !auth.jePrijavljenKorisnik) {
    return '/prijava'
  }
})

export default router

<template>
  <v-navigation-drawer permanent>
    <v-list-item title="Admin panel" nav></v-list-item>
    <v-divider></v-divider>
    <v-list density="compact" nav>
      <v-list-item title="Dashboard" to="/admin" prepend-icon="mdi-view-dashboard"></v-list-item>
      <v-list-item title="Putovi" to="/admin/putovi" prepend-icon="mdi-airplane"></v-list-item>
      <v-list-item title="Vodiči" to="/admin/vodici" prepend-icon="mdi-account-tie"></v-list-item>
      <v-list-item title="Rezervacije" to="/admin/rezervacije" prepend-icon="mdi-calendar-check"></v-list-item>
      <v-list-item title="Korisnici" to="/admin/korisnici" prepend-icon="mdi-account-group"></v-list-item>
    </v-list>
    <template v-slot:append>
      <v-list density="compact" nav>
        <v-list-item title="Na stranicu" to="/" prepend-icon="mdi-home"></v-list-item>
      </v-list>
    </template>
  </v-navigation-drawer>

  <v-main>
    <v-container class="mt-4">
      <slot />
    </v-container>
  </v-main>
</template>

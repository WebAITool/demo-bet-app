<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const showAppShell = computed(() => !route.path.startsWith('/auth'))
</script>

<template>
  <v-app>
    <v-app-bar v-if="showAppShell" flat>
      <v-spacer />
      <v-btn color="info" :to="{ name: 'Account' }">Мой аккаунт</v-btn>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
    <v-footer v-if="showAppShell" app height="48" class="d-flex align-center justify-center">
      <span class="text-caption">© {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
  
</template>

<style scoped>
</style>

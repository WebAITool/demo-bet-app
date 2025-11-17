<script setup>
import { ref, onMounted } from 'vue'
import { userApi, betsApi } from '@/api/api'

const loading = ref(true)
const error = ref(null)
const balance = ref(null)
const bets = ref([])

const load = async () => {
  loading.value = true
  error.value = null
  try {
    const [b, my] = await Promise.all([
      userApi.getBalance(),
      betsApi.getMyBets(),
    ])
    balance.value = Number(b.data)
    bets.value = Array.isArray(my.data) ? my.data : []
  } catch (e) {
    error.value = 'Не удалось загрузить данные аккаунта'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <v-container class="py-8">
    <v-row class="mb-6">
      <v-col cols="12" md="4">
        <v-btn block color="primary" variant="outlined" :to="{ name: 'AccountInfo' }" prepend-icon="mdi-account-circle" size="large">Личные данные</v-btn>
      </v-col>
      <v-col cols="12" md="4">
        <v-card elevation="2" class="pa-4 d-flex align-center justify-space-between">
          <div class="text-medium-emphasis">Баланс</div>
          <div class="text-h6">{{ balance == null ? '—' : balance + ' Ф' }}</div>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-btn block color="pink-lighten-3" variant="outlined" prepend-icon="mdi-calendar" size="large" :to="{ name: 'MyEvents' }">Мои события</v-btn>
      </v-col>
    </v-row>

    <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>
    <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />

    <v-card elevation="2">
      <v-card-title>История ставок</v-card-title>
      <v-divider />
      <v-table>
        <thead>
          <tr>
            <th>Событие</th>
            <th>Размер</th>
            <th>Исход</th>
            <th>Итог</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!bets.length">
            <td colspan="4" class="text-medium-emphasis">Ставок пока нет</td>
          </tr>
          <tr v-for="(row, idx) in bets" :key="idx">
            <td>{{ row.event_name }}</td>
            <td>{{ row.size }} Ф</td>
            <td>{{ row.outcome_name ?? '—' }}</td>
            <td>{{ row.final_outcome_name ?? '—' }}</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

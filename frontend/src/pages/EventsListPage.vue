<script setup>
import { ref, onMounted } from 'vue'
import { eventsApi } from '@/api/api'

const loading = ref(true)
const error = ref(null)
const events = ref([])

const load = async () => {
  loading.value = true
  error.value = null
  try {
    const { data } = await eventsApi.getAll()
    events.value = Array.isArray(data) ? data : []
  } catch (e) {
    error.value = 'Не удалось загрузить события'
  } finally {
    loading.value = false
  }
}

const formatDate = (v) => {
  try {
    return new Date(v).toLocaleString('ru-RU', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
  } catch {
    return v
  }
}

onMounted(load)
</script>

<template>
  <v-container class="py-8">
    <v-card elevation="2">
      <v-card-title class="text-h6">Список доступных для ставок событий</v-card-title>
      <v-divider />

      <v-progress-linear v-if="loading" indeterminate color="primary" />
      <v-alert v-else-if="error" type="error" density="comfortable">{{ error }}</v-alert>

      <v-table v-else density="comfortable" class="text-no-wrap">
        <thead>
          <tr>
            <th class="text-left" style="width:45%">Название события</th>
            <th class="text-left" style="width:20%">Время окончания</th>
            <th class="text-right" style="width:35%">Исходы</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ev in events" :key="ev.event_id">
            <td>
              <router-link :to="{ name: 'EventDetails', params: { id: ev.event_id } }" class="text-decoration-none">
                {{ ev.name }}
              </router-link>
            </td>
            <td>{{ formatDate(ev.ended_at) }}</td>
            <td class="text-right">
              <v-chip
                v-for="(o, idx) in ev.outcomes"
                :key="idx"
                class="ml-1"
                size="small"
                color="primary"
                variant="outlined"
                :to="{ name: 'EventDetails', params: { id: ev.event_id }, query: { outcome: idx } }"
              >
                {{ o.name }} — {{ Number(o.coefficient).toFixed(2) }}
              </v-chip>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

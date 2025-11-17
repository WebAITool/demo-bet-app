<script setup>
import { ref, onMounted, onActivated } from 'vue'
import { useRouter } from 'vue-router'
import { eventsApi } from '@/api/api'

const router = useRouter()

const loading = ref(true)
const error = ref(null)
const events = ref([])

const loadEvents = async () => {
  loading.value = true
  error.value = null
  try {
    const { data } = await eventsApi.getMy()
    const arr = Array.isArray(data) ? data : []
    events.value = arr.slice().sort((a, b) => (b.event_id ?? 0) - (a.event_id ?? 0))
  } catch (e) {
    error.value = 'Не удалось загрузить ваши события'
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

const editEvent = (eventId) => {
  router.push({ name: 'EditEvent', params: { id: eventId } })
}

onMounted(loadEvents)
onActivated(loadEvents)
</script>

<template>
  <v-container class="py-8">
    <v-card elevation="2">
      <v-card-title>Мои события</v-card-title>
      <v-divider />

      <v-progress-linear v-if="loading" indeterminate color="primary" />
      <v-alert v-else-if="error" type="error">{{ error }}</v-alert>

      <v-list v-else>
        <v-list-item v-for="ev in events" :key="ev.event_id">
          <v-list-item-title>{{ ev.name }}</v-list-item-title>
          <v-list-item-subtitle>
            Окончание ставок: {{ formatDate(ev.ended_at) }}
          </v-list-item-subtitle>
          <template #append>
            <v-btn color="primary" variant="tonal" class="mr-2" :to="{ name: 'EditEvent', params: { id: ev.event_id } }">Редактировать</v-btn>
            <v-chip v-if="ev.final_outcome_name" color="green" variant="outlined">Итог: {{ ev.final_outcome_name }}</v-chip>
          </template>
        </v-list-item>
        <v-list-item v-if="!events.length" title="Событий пока нет" />
      </v-list>

      <v-divider />
      <div class="pa-4 d-flex justify-end">
        <v-btn color="indigo" :to="{ name: 'CreateEvent' }" prepend-icon="mdi-plus">Создать событие</v-btn>
      </div>
    </v-card>
  </v-container>
</template>

<style scoped>
.v-list-item { border-bottom: 1px solid rgba(0,0,0,0.1); }
.v-list-item:last-child { border-bottom: none; }
</style>

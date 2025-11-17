<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { eventsApi } from '@/api/api'

const route = useRoute()
const router = useRouter()

const eventId = ref(null)
const loading = ref(true)
const saving = ref(false)
const error = ref(null)
const message = ref(null)

const eventName = ref('')
const eventDescription = ref('')
const endedAt = ref('')
const outcomes = ref([])
const finalOutcomeId = ref(null)

const loadEvent = async () => {
  loading.value = true
  error.value = null
  try {
    const id = Number(route.params.id)
    eventId.value = id
    const { data } = await eventsApi.getById(id)
    eventName.value = data.name || ''
    eventDescription.value = data.description || ''
    endedAt.value = data.ended_at || ''
    finalOutcomeId.value = data.final_outcome_id ?? null
    outcomes.value = (data.outcomes || []).map(o => ({ outcome_id: o.outcome_id, name: o.name, coefficient: Number(o.coefficient) }))
  } catch (e) {
    error.value = 'Не удалось загрузить событие'
  } finally {
    loading.value = false
  }
}

const saveCoefficients = async () => {
  if (!eventId.value) return
  saving.value = true
  error.value = null
  message.value = null
  try {
    const payload = { outcomes: outcomes.value.map(o => ({ outcome_id: o.outcome_id, coefficient: Number(o.coefficient) })) }
    await eventsApi.updateEvent(eventId.value, payload)
    message.value = 'Коэффициенты обновлены'
    await loadEvent()
  } catch (e) {
    const s = e?.response?.status
    if (s === 400) error.value = 'Неверные данные'
    else if (s === 403) error.value = 'Недостаточно прав (не автор)'
    else if (s === 404) error.value = 'Событие или исход не найден'
    else error.value = 'Не удалось обновить коэффициенты'
  } finally {
    saving.value = false
  }
}

const setFinalOutcome = async () => {
  if (!eventId.value) return
  saving.value = true
  error.value = null
  message.value = null
  try {
    await eventsApi.updateEvent(eventId.value, { final_outcome_id: finalOutcomeId.value })
    message.value = 'Финальный исход установлен'
    await loadEvent()
  } catch (e) {
    const s = e?.response?.status
    if (s === 400) error.value = 'Неверные данные'
    else if (s === 403) error.value = 'Недостаточно прав (не автор)'
    else if (s === 404) error.value = 'Событие или исход не найден'
    else if (s === 409) error.value = 'Финальный исход уже установлен'
    else error.value = 'Не удалось установить финальный исход'
  } finally {
    saving.value = false
  }
}

onMounted(loadEvent)
</script>

<template>
  <v-container class="py-8">
    <h1 class="mb-4">Редактирование события</h1>

    <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>
    <v-alert v-if="message" type="success" class="mb-4">{{ message }}</v-alert>
    <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />

    <v-row v-if="!loading && !error">
      <v-col cols="12" md="8">
        <v-card class="mb-4">
          <v-card-text>
            <v-text-field
              v-model="eventName"
              label="Название"
              variant="outlined"
              class="mb-4"
              hide-details
              disabled
            />

            <v-list>
              <v-list-item
                v-for="o in outcomes"
                :key="o.outcome_id"
                class="d-flex align-center"
              >
                <v-list-item-title class="mr-4">{{ o.name }}</v-list-item-title>
                <v-text-field
                  v-model.number="o.coefficient"
                  label="Коэффициент"
                  type="number"
                  min="1.01"
                  step="0.1"
                  variant="outlined"
                  density="compact"
                  hide-details
                  style="max-width: 140px"
                />
              </v-list-item>
            </v-list>

            <div class="d-flex justify-end mt-4">
              <v-btn color="primary" @click="saveCoefficients" :loading="saving" :disabled="saving">Сохранить коэффициенты</v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card elevation="2" class="mb-4">
          <v-card-title class="text-subtitle-1">Финальный исход</v-card-title>
          <v-card-text>
            <v-select
              :items="outcomes.map(o => ({ title: o.name, value: o.outcome_id }))"
              v-model="finalOutcomeId"
              label="Выберите исход"
              variant="outlined"
              hide-details
            />
            <v-btn class="mt-2" color="success" @click="setFinalOutcome" :loading="saving" :disabled="saving">Установить</v-btn>
            <div class="text-caption text-medium-emphasis mt-2">Текущее значение: {{ finalOutcomeId ?? 'не задан' }}</div>
          </v-card-text>
        </v-card>
        <v-card elevation="2">
          <v-card-title class="text-subtitle-1">Информация</v-card-title>
          <v-card-text>
            Завершение ставок: {{ new Date(endedAt).toLocaleString('ru-RU') }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { eventsApi, betsApi } from '@/api/api'

const route = useRoute()
const loading = ref(true)
const error = ref(null)
const eventData = ref(null)
const eventId = ref(null)
const selectedIdx = ref(null)
const betAmount = ref('')
const placing = ref(false)
const message = ref(null)
const suggestions = [100, 200, 300, 500, 1000]

const bettors = ref([])
const bettorsLoading = ref(false)
const bettorsError = ref(null)

const loadEvent = async () => {
  loading.value = true
  error.value = null
  try {
    const id = Number(route.params.id)
    eventId.value = id
    const { data } = await eventsApi.getById(id)
    eventData.value = data
    const q = route.query.outcome
    if (q != null && !Number.isNaN(parseInt(q))) selectedIdx.value = parseInt(q)
  } catch (e) {
    error.value = 'Событие не найдено'
  } finally {
    loading.value = false
  }
}

const selectOutcome = (idx) => {
  selectedIdx.value = idx
  const url = new URL(window.location.href)
  url.searchParams.set('outcome', String(idx))
  window.history.pushState({}, '', url)
}

const loadBettors = async () => {
  bettors.value = []
  bettorsError.value = null
  if (eventData.value == null || selectedIdx.value == null) return
  const outcome = eventData.value.outcomes[selectedIdx.value]
  if (!outcome) return
  bettorsLoading.value = true
  try {
    const { data } = await betsApi.getByOutcome(eventId.value, outcome.outcome_id)
    bettors.value = Array.isArray(data) ? data : []
  } catch (e) {
    const s = e?.response?.status
    if (s === 404) {
      bettors.value = []
      bettorsError.value = null
    } else {
      bettorsError.value = 'Не удалось получить список ставок'
    }
  } finally {
    bettorsLoading.value = false
  }
}

watch(selectedIdx, loadBettors)

const placeBet = async () => {
  if (!eventData.value || selectedIdx.value == null) return
  const amount = Number(betAmount.value)
  if (!amount || amount <= 0) return
  const outcome = eventData.value.outcomes[selectedIdx.value]
  placing.value = true
  message.value = null
  error.value = null
  try {
    await betsApi.placeBet({ event_id: eventId.value, outcome_id: outcome.outcome_id, size: amount })
    message.value = 'Ставка принята'
    betAmount.value = ''
    await loadBettors()
  } catch (e) {
    const s = e?.response?.status
    if (s === 403) error.value = 'Ставки закрыты'
    else if (s === 404) error.value = 'Событие или исход не найден'
    else if (s === 409) error.value = 'Недостаточно средств'
    else error.value = 'Не удалось сделать ставку'
  } finally {
    placing.value = false
  }
}

onMounted(async () => {
  await loadEvent()
  await loadBettors()
})
</script>

<template>
  <v-container class="py-8">
    <v-progress-linear v-if="loading" indeterminate color="primary" />
    <v-alert v-else-if="error" type="error" class="mb-4">{{ error }}</v-alert>

    <template v-else>
      <h1 class="mb-2">{{ eventData.name }}</h1>
      <p class="mb-6">{{ eventData.description }}</p>

      <v-row>
        <v-col cols="12" md="7">
          <v-card class="mb-4" elevation="2">
            <v-card-title v-if="selectedIdx == null">Выберите исход, чтобы видеть список ставок</v-card-title>
            <v-card-title v-else>Список тех, кто поставил на выбранный исход</v-card-title>
            <v-divider />
            
            <v-card-text v-if="selectedIdx == null">
              <div class="text-medium-emphasis">Пока исход не выбран, список ставок не отобразится</div>
            </v-card-text>

            <v-card-text v-else>
              <v-alert v-if="bettorsError" type="error" density="compact" class="mb-2">{{ bettorsError }}</v-alert>
              <v-progress-linear v-if="bettorsLoading" indeterminate color="primary" />
              <v-list v-else>
                <v-list-item v-if="!bettors.length" title="Нет ставок" />
                <v-list-item v-for="b in bettors" :key="b.id ?? (b.login + '-' + b.size)">
                  <v-list-item-title>{{ b.login }}</v-list-item-title>
                  <v-list-item-subtitle>{{ b.size }} Ф</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="5">
          <v-card class="mb-4" elevation="2">
            <v-card-title>Исходы</v-card-title>
            <v-divider />
            <v-card-text>
              <v-btn
                v-for="(o, idx) in eventData.outcomes"
                :key="o.outcome_id"
                block class="mb-2"
                :variant="selectedIdx === idx ? 'outlined' : 'elevated'"
                color="amber"
                @click="selectOutcome(idx)"
              >{{ o.name }} — {{ Number(o.coefficient).toFixed(2) }}</v-btn>
            </v-card-text>
          </v-card>

          <div class="betting-controls">
            <div class="bet-amount-input mb-4">
              <v-text-field
                v-model="betAmount"
                label="Размер ставки"
                type="number"
                min="1"
                variant="outlined"
                hide-details
                density="comfortable"
              >
                <template #append-inner>
                  <span class="text-amber-darken-3 font-weight-bold">Ф</span>
                </template>
              </v-text-field>
            </div>
            
            <div class="suggestion-buttons mb-6">
              <div class="d-flex gap-2 flex-wrap justify-center">
                <v-chip
                  v-for="amount in suggestions"
                  :key="amount"
                  variant="outlined"
                  class="suggestion-chip"
                  @click="betAmount = String(amount)"
                  size="large"
                >
                  {{ amount }} Ф
                </v-chip>
              </div>
            </div>
            
            <div class="place-bet-button">
              <v-btn 
                color="primary" 
                size="x-large"
                block
                :disabled="!betAmount || betAmount <= 0 || selectedIdx == null"
                class="font-weight-bold"
                height="48"
                :loading="placing"
                @click="placeBet"
              >
                Сделать ставку
              </v-btn>
              <div class="mt-2">
                <v-alert v-if="message" type="success" density="compact">{{ message }}</v-alert>
              </div>
            </div>
          </div>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

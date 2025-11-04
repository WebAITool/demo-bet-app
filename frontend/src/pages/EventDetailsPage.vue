<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const selected = ref(null)
const betAmount = ref('')
const suggestions = [100, 200, 300, 500, 1000]

onMounted(() => {
  if (route.query.outcome) {
    selected.value = parseInt(route.query.outcome) + 1
  }
})
const outcomes = [
  { id: 1, label: 'Исход 1', coef: 'коэф' },
  { id: 2, label: 'Исход 2', coef: 'коэф' },
  { id: 3, label: 'Исход 3', coef: 'коэф' },
]
function selectOutcome(id) { 
  selected.value = id 
  const newUrl = new URL(window.location.href)
  newUrl.searchParams.set('outcome', id - 1)
  window.history.pushState({}, '', newUrl)
}
</script>

<template>
  <v-container class="py-8">
    <h1 class="mb-2">Название</h1>
    <p class="mb-6">Описание</p>

    <v-row>
      <v-col cols="12" md="7">
        <v-card class="mb-4" elevation="2">
          <v-card-title>Список тех, кто поставил на выбранный исход</v-card-title>
          <v-divider />
          <v-list>
            <v-list-item v-for="n in 6" :key="n">
              <v-list-item-title>логин {{ n }}</v-list-item-title>
              <v-list-item-subtitle>размер ставки</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
      <v-col cols="12" md="5">
        <v-card class="mb-4" elevation="2">
          <v-card-title>Исходы</v-card-title>
          <v-divider />
          <v-card-text>
            <v-btn
              v-for="o in outcomes"
              :key="o.id"
              block class="mb-2"
              :variant="selected === o.id ? 'outlined' : 'elevated'"
              color="amber"
              @click="selectOutcome(o.id)"
            >{{ o.label }}
              — {{ o.coef }}</v-btn>
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
              <template v-slot:append-inner>
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
                @click="betAmount = amount"
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
              :disabled="!betAmount || betAmount <= 0"
              class="font-weight-bold"
              height="48"
            >
              Сделать ставку
            </v-btn>
          </div>
        </div>
      </v-col>
    </v-row>

  </v-container>
</template>

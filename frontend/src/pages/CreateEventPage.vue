<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const eventTitle = ref('');
const newOutcome = ref('');
const newCoefficient = ref('2.0');
const eventDate = ref(new Date().toISOString().split('T')[0]);
const eventTime = ref('12:00');
const outcomes = ref([
  { id: 1, name: 'Исход 1', coefficient: 2.0 },
  { id: 2, name: 'Исход 2', coefficient: 2.0 },
  { id: 3, name: 'Исход 3', coefficient: 2.0 }
]);

const addOutcome = () => {
  const coefficient = parseFloat(newCoefficient.value);
  if (newOutcome.value.trim() && !isNaN(coefficient) && coefficient > 0) {
    outcomes.value.push({
      id: Date.now(),
      name: newOutcome.value,
      coefficient: coefficient
    });
    newOutcome.value = '';
    newCoefficient.value = '2.0';
  } else {
    alert('Пожалуйста, укажите название исхода и корректный коэффициент (число больше 0)');
  }
};

const removeOutcome = (id) => {
  outcomes.value = outcomes.value.filter(outcome => outcome.id !== id);
};

const formatDateTime = () => {
  const [year, month, day] = eventDate.value.split('-');
  const [hours, minutes] = eventTime.value.split(':');
  const date = new Date(year, month - 1, day, hours, minutes);
  
  if (isNaN(date.getTime())) return 'Некорректная дата';
  
  const options = { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };
  return date.toLocaleString('ru-RU', options);
};

const createEvent = () => {
  if (!eventTitle.value.trim() || outcomes.value.length < 2) {
    alert('Пожалуйста, укажите название события и минимум 2 исхода');
    return;
  }
  
  const [year, month, day] = eventDate.value.split('-');
  const [hours, minutes] = eventTime.value.split(':');
  const endsAtDate = new Date(year, month - 1, day, hours, minutes);
  
  if (endsAtDate < new Date()) {
    alert('Дата окончания не может быть в прошлом');
    return;
  }

  const events = JSON.parse(localStorage.getItem('myEvents') || '[]');
  
  const newEvent = {
    id: Date.now(),
    title: eventTitle.value,
    outcomes: [...outcomes.value],
    endsAt: endsAtDate.toISOString(),
    status: 'editing'
  };

  events.push(newEvent);
  localStorage.setItem('myEvents', JSON.stringify(events));
  
  router.push({ name: 'MyEvents' });
};
</script>

<template>
  <v-container class="py-8">
    <h1 class="mb-4">Создание события</h1>
    
    <v-text-field
      v-model="eventTitle"
      label="Название события"
      class="mb-4"
      variant="outlined"
    ></v-text-field>

    <v-row>
      <v-col cols="12" md="6">
        <h3 class="text-subtitle-1 mb-2">Исходы</h3>
        <v-card class="mb-4" elevation="2">
          <v-list>
            <v-list-item 
              v-for="outcome in outcomes" 
              :key="outcome.id"
              class="d-flex justify-space-between align-center"
            >
              <div class="d-flex align-center gap-2">
                <span>{{ outcome.name }}</span>
                <v-chip size="small" color="primary" variant="outlined">
                  {{ outcome.coefficient.toFixed(2) }}
                </v-chip>
              </div>
              <v-btn
                icon
                variant="text"
                color="error"
                size="small"
                @click="removeOutcome(outcome.id)"
                v-if="outcomes.length > 2"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-list-item>
          </v-list>
          <div class="pa-4">
            <div class="d-flex gap-2 align-center mb-2">
              <v-text-field 
                v-model="newOutcome"
                label="Название исхода"
                variant="outlined"
                density="compact"
                hide-details
                @keyup.enter="addOutcome"
                class="flex-grow-1"
              />
              <v-text-field 
                v-model="newCoefficient"
                label="Коеф."
                type="number"
                min="1.01"
                step="0.1"
                variant="outlined"
                density="compact"
                hide-details
                style="max-width: 120px"
                @keyup.enter="addOutcome"
              />
            </div>
            <v-btn 
              block
              class="mt-2" 
              variant="tonal"
              @click="addOutcome"
              :disabled="!newOutcome.trim() || !newCoefficient || parseFloat(newCoefficient) <= 1"
            >
              Добавить исход
            </v-btn>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card elevation="2" class="mb-4">
          <v-card-title class="text-subtitle-1">Время окончания ставок</v-card-title>
          <v-card-text>
            <v-date-picker
              v-model="eventDate"
              :min="new Date().toISOString().split('T')[0]"
              :max="new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]"
              full-width
              variant="outlined"
              class="mb-2"
              hide-actions
            />
            <v-text-field
              v-model="eventTime"
              type="time"
              label="Время окончания"
              variant="outlined"
              density="compact"
              hide-details
              class="mb-2"
            />
            <div class="text-caption text-medium-emphasis">
              Итоговое время: {{ formatDateTime() }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <div class="d-flex justify-end mt-6">
      <v-btn 
        color="primary"
        @click="createEvent"
        :disabled="!eventTitle.trim() || outcomes.length < 2"
      >
        Создать событие
      </v-btn>
    </div>

  </v-container>
</template>

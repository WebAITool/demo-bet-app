<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const event = ref({
  id: null,
  title: '',
  outcomes: [],
  endsAt: new Date().toISOString(),
  status: 'editing'
});

const eventDate = ref('');
const eventTime = ref('12:00');

const formatDateTimeForInput = (dateString) => {
  const date = new Date(dateString);
  return {
    date: date.toISOString().split('T')[0],
    time: `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
  };
};

onMounted(() => {
  const events = JSON.parse(localStorage.getItem('myEvents') || '[]');
  const foundEvent = events.find(e => e.id === parseInt(route.params.id));
  
  if (foundEvent) {
    event.value = { ...foundEvent };
    event.value.outcomes = foundEvent.outcomes.map(outcome => ({
      ...outcome,
      id: outcome.id || Date.now() + Math.random()
    }));
    
    const { date, time } = formatDateTimeForInput(event.value.endsAt);
    eventDate.value = date;
    eventTime.value = time;
  } else {
    router.push({ name: 'MyEvents' });
  }
});

const updateOutcome = (outcomeId, field, value) => {
  const outcome = event.value.outcomes.find(o => o.id === outcomeId);
  if (outcome) {
    outcome[field] = field === 'coefficient' ? parseFloat(value) : value;
  }
};

const saveEvent = () => {
  const [year, month, day] = eventDate.value.split('-');
  const [hours, minutes] = eventTime.value.split(':');
  const endsAtDate = new Date(year, month - 1, day, hours, minutes);
  
  if (endsAtDate < new Date()) {
    alert('Дата окончания не может быть в прошлом');
    return;
  }
  
  event.value.endsAt = endsAtDate.toISOString();
  
  const events = JSON.parse(localStorage.getItem('myEvents') || '[]');
  const index = events.findIndex(e => e.id === event.value.id);
  
  if (index !== -1) {
    events[index] = { ...event.value };
    localStorage.setItem('myEvents', JSON.stringify(events));
    router.push({ name: 'MyEvents' });
  }
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

const formatDate = (dateString) => {
  const options = { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };
  return new Date(dateString).toLocaleString('ru-RU', options);
};
</script>

<template>
  <v-container class="py-8">
    <div class="d-flex justify-space-between align-center mb-4">
      <h1>Изменение события</h1>
      <v-btn 
        color="primary" 
        @click="saveEvent"
        :disabled="!event.title.trim() || event.outcomes.length < 2"
      >
        Сохранить изменения
      </v-btn>
    </div>

    <v-row>
      <v-col cols="12" md="8">
        <v-card class="mb-4">
          <v-card-text>
            <v-text-field
              v-model="event.title"
              label="Название события"
              variant="outlined"
              class="mb-4"
              hide-details
            />
            
            <v-list>
              <v-list-item 
                v-for="outcome in event.outcomes" 
                :key="outcome.id"
                class="d-flex align-center"
              >
                <v-text-field
                  v-model="outcome.name"
                  label="Название исхода"
                  variant="outlined"
                  density="compact"
                  hide-details
                  class="mr-2"
                  @update:modelValue="val => updateOutcome(outcome.id, 'name', val)"
                />
                <v-text-field
                  v-model.number="outcome.coefficient"
                  label="Коэффициент"
                  type="number"
                  min="1.01"
                  step="0.1"
                  variant="outlined"
                  density="compact"
                  hide-details
                  style="max-width: 120px"
                  @update:modelValue="val => updateOutcome(outcome.id, 'coefficient', val)"
                />
                <v-chip class="ml-2" color="primary" variant="outlined">
                  {{ outcome.coefficient.toFixed(2) }}
                </v-chip>
              </v-list-item>
            </v-list>
          </v-card-text>
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

  </v-container>
</template>

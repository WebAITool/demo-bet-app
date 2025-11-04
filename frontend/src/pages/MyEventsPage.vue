<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// Состояния события:
// 1. 'editing' - можно редактировать (время ставок не закончилось)
// 2. 'setting_outcome' - нужно задать исход (время ставок закончилось, но исход не задан)
// 3. 'completed' - исход задан (показываем результат)

const events = ref([]);

onMounted(() => {
  loadEvents();
});

const loadEvents = () => {
  const savedEvents = localStorage.getItem('myEvents');
  if (savedEvents) {
    events.value = JSON.parse(savedEvents);
  }
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

const setOutcome = (event) => {
  const outcome = prompt('Введите итоговый исход события:');
  if (outcome) {
    const updatedEvents = events.value.map(e => 
      e.id === event.id ? { ...e, outcome, status: 'completed' } : e
    );
    
    localStorage.setItem('myEvents', JSON.stringify(updatedEvents));
    
    const eventIndex = events.value.findIndex(e => e.id === event.id);
    if (eventIndex !== -1) {
      events.value[eventIndex].outcome = outcome;
      events.value[eventIndex].status = 'completed';
    }
  }
};

const editEvent = (eventId) => {
  router.push({ name: 'EditEvent', params: { id: eventId } });
};
</script>

<template>
  <v-container class="py-8">
    <v-card elevation="2">
      <v-card-title>Мои события</v-card-title>
      <v-divider />
      <v-list>
        <v-list-item v-for="event in events" :key="event.id">
          <v-list-item-title>{{ event.title }}</v-list-item-title>
          <v-list-item-subtitle>
            Окончание ставок: {{ formatDate(event.endsAt) }}
          </v-list-item-subtitle>
          
          <template #append>
            <v-btn 
              v-if="event.status === 'editing'"
              class="mr-2" 
              variant="tonal"
              color="primary"
              @click="editEvent(event.id)"
            >
              Изменить событие
            </v-btn>
            
            <v-btn 
              v-else-if="event.status === 'setting_outcome'"
              class="mr-2" 
              color="pink" 
              variant="elevated"
              @click="setOutcome(event)"
            >
              Задать исход
            </v-btn>
            
            <div v-else-if="event.status === 'completed'" class="text-body-1">
              Итоговый исход: {{ event.outcome }}
            </div>
          </template>
        </v-list-item>
      </v-list>
      <v-divider />
      <div class="pa-4 d-flex justify-end">
        <v-btn color="indigo" :to="{ name: 'CreateEvent' }" prepend-icon="mdi-plus">
          Создать событие
        </v-btn>
      </div>
    </v-card>
  </v-container>
</template>

<style scoped>
.v-list-item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.v-list-item:last-child {
  border-bottom: none;
}
</style>

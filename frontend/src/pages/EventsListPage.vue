<script setup>
const events = [
  { id: 1, title: 'Событие 1', endsAt: 'Сегодня 21:00' },
  { id: 2, title: 'Событие 2', endsAt: 'Сегодня 22:30' },
  { id: 3, title: 'Событие 3', endsAt: 'Завтра 19:00' },
  { id: 4, title: 'Событие 4', endsAt: 'Завтра 20:15' },
  { id: 5, title: 'Событие 5', endsAt: 'Через 2 дня 18:00' },
]
</script>

<template>
  <v-container class="py-8">
    <v-card elevation="2">
      <v-card-title class="text-h6">Список доступных для ставок событий</v-card-title>
      <v-divider />
      <v-table density="comfortable" class="text-no-wrap">
        <thead>
          <tr>
            <th class="text-left" style="width:45%">Название события</th>
            <th class="text-left" style="width:20%">Время окончания</th>
            <th class="text-right" style="width:35%">Исходы</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ev in events" :key="ev.id">
            <td>
              <router-link :to="{ name: 'EventDetails', params: { id: ev.id } }" class="text-decoration-none">
                {{ ev.title }}
              </router-link>
            </td>
            <td>{{ ev.endsAt }}</td>
            <td class="text-right">
              <v-btn variant="text" class="mr-1" color="primary" :to="{ name: 'EventDetails', params: { id: ev.id }, query: { outcome: 0 } }">Исход1 - коэф</v-btn>
              <v-btn variant="text" class="mr-1" color="primary" :to="{ name: 'EventDetails', params: { id: ev.id }, query: { outcome: 1 } }">Исход2 - коэф</v-btn>
              <v-btn variant="text" color="primary" :to="{ name: 'EventDetails', params: { id: ev.id }, query: { outcome: 2 } }">Исход3 - коэф</v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

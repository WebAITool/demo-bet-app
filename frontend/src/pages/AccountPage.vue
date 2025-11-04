<template>
  <v-container class="py-8">
    <v-row class="mb-6">
      <v-col cols="12" md="4">
        <v-btn 
          block 
          color="primary" 
          variant="outlined"
          :to="{ name: 'AccountInfo' }"
          prepend-icon="mdi-account-circle"
          size="large"
        >
          Личные данные
        </v-btn>
      </v-col>
      <v-col cols="12" md="4">
        <v-btn 
          block 
          color="yellow" 
          variant="outlined"
          prepend-icon="mdi-cash"
          size="large"
        >
          Баланс
        </v-btn>
      </v-col>
      <v-col cols="12" md="4">
        <v-btn 
          block 
          color="pink-lighten-3" 
          variant="outlined"
          prepend-icon="mdi-calendar"
          size="large"
          :to="{ name: 'MyEvents' }"
        >
          Мои события
        </v-btn>
      </v-col>
    </v-row>

    <v-card class="mt-8" elevation="2">
      <v-card-title>История ставок</v-card-title>
      <v-divider />
      <v-table>
        <thead>
          <tr>
            <th>Название события</th>
            <th>Ставка</th>
            <th>Итог</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="n in 4" :key="n">
            <td>Событие {{ n }}</td>
            <td>100 на Исход 2</td>
            <td>???</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

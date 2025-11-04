<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center" class="w-100">
      <v-col cols="12" sm="8" md="5" lg="4">
        <v-card elevation="2" class="pa-6">
          <h2 class="text-h5 mb-6 text-center">Вход</h2>
          <v-form>
            <v-text-field label="Логин" prepend-inner-icon="mdi-account" required density="comfortable" />
            <v-text-field label="Пароль" type="password" prepend-inner-icon="mdi-lock" required density="comfortable" />
            <div class="d-flex justify-center mt-2">
              <v-btn color="primary" :to="{ name: 'EventsList' }">Войти</v-btn>
            </div>
            <div class="text-center mt-4">
              <span class="mr-2">Нет аккаунта?</span>
              <v-btn color="primary" variant="text" :to="{ name: 'Register' }">Зарегистрироваться</v-btn>
            </div>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

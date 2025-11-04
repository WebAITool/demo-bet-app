<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center" class="w-100">
      <v-col cols="12" sm="8" md="6" lg="5">
        <v-card elevation="2" class="pa-6">
          <h2 class="text-h5 mb-6 text-center">Регистрация</h2>
          <v-form>
            <v-text-field label="Логин" prepend-inner-icon="mdi-account" required density="comfortable" />
            <v-text-field label="Пароль" type="password" prepend-inner-icon="mdi-lock" required density="comfortable" />
            <v-text-field 
              label="Email" 
              type="email" 
              prepend-inner-icon="mdi-email" 
              required 
              density="comfortable" 
              class="mt-2"
            />
            <div class="d-flex justify-center mt-2 mb-4">
              <v-btn 
                color="secondary" 
                variant="elevated"
              >
                Отправить код
              </v-btn>
            </div>
            <v-text-field class="mt-4" label="Код из email" required density="comfortable" />
            <div class="d-flex justify-center mt-2">
              <v-btn color="success" :to="{ name: 'Login' }">Подтвердить</v-btn>
            </div>
            <div class="text-center mt-4">
              <span class="mr-2">Есть аккаунт?</span>
              <v-btn color="primary" variant="text" :to="{ name: 'Login' }">Войти</v-btn>
            </div>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

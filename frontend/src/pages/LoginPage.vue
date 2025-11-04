<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const auth = useAuthStore();
const loginValue = ref('');
const passwordValue = ref('');
const showPassword = ref(false);

const onSubmit = async () => {
  const ok = await auth.login({ login: loginValue.value.trim(), password: passwordValue.value });
  if (ok) {
    await router.replace({ name: 'EventsList' });
  }
};
</script>

<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center" class="w-100">
      <v-col cols="12" sm="8" md="5" lg="4">
        <v-card elevation="2" class="pa-6">
          <h2 class="text-h5 mb-6 text-center">Вход</h2>
          <v-form @submit.prevent="onSubmit">
            <v-text-field
              v-model="loginValue"
              label="Логин"
              prepend-inner-icon="mdi-account"
              required
              density="comfortable"
              autocomplete="username"
            />
            <v-text-field
              v-model="passwordValue"
              :type="showPassword ? 'text' : 'password'"
              label="Пароль"
              prepend-inner-icon="mdi-lock"
              :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showPassword = !showPassword"
              required
              density="comfortable"
              autocomplete="current-password"
            />

            <div v-if="auth.error" class="text-error text-center mb-2">{{ auth.error }}</div>

            <div class="d-flex justify-center mt-2">
              <v-btn type="submit" color="primary" :loading="auth.loading" :disabled="!loginValue || !passwordValue" @click="onSubmit">
                Войти
              </v-btn>
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

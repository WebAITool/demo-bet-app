<script setup>
import { ref, onMounted } from 'vue'
import { userApi } from '@/api/api'

const loading = ref(true)
const error = ref(null)
const message = ref(null)

const login = ref('')
const password = ref('')

const editing = ref(null)
const temp = ref('')

const loadInfo = async () => {
  loading.value = true
  error.value = null
  try {
    const { data } = await userApi.getInfo()
    login.value = data?.login ?? ''
  } catch (e) {
    error.value = 'Не удалось загрузить профиль'
  } finally {
    loading.value = false
  }
}

const startEdit = (field) => {
  editing.value = field
  temp.value = field === 'login' ? login.value : ''
}

const cancelEdit = () => {
  editing.value = null
  temp.value = ''
}

const save = async () => {
  if (!editing.value) return
  error.value = null
  message.value = null
  try {
    const payload = {}
    if (editing.value === 'login') payload.login = String(temp.value).trim()
    if (editing.value === 'password') payload.password = String(temp.value)
    await userApi.updateInfo(payload)
    if (payload.login) login.value = payload.login
    if (payload.password) password.value = ''
    message.value = 'Изменения сохранены'
    cancelEdit()
  } catch (e) {
    error.value = 'Не удалось сохранить изменения'
  }
}

onMounted(loadInfo)
</script>

<template>
  <v-container class="py-8">
    <v-card class="pa-6">
      <v-card-title class="text-h5 mb-6">Профиль</v-card-title>
      <v-divider class="mb-4" />

      <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>
      <v-alert v-if="message" type="success" class="mb-4">{{ message }}</v-alert>
      <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />

      <v-form v-if="!loading">
        <v-card variant="outlined" class="mb-4">
          <v-card-text>
            <div class="d-flex align-center">
              <div class="flex-grow-1">
                <div class="text-caption text-grey">Login</div>
                <template v-if="editing !== 'login'">
                  <div class="text-body-1">{{ login || '—' }}</div>
                </template>
                <v-text-field
                  v-else
                  v-model="temp"
                  variant="outlined"
                  density="compact"
                  hide-details
                  autofocus
                  @keyup.enter="save"
                  @keyup.esc="cancelEdit"
                />
              </div>
              <v-btn v-if="editing !== 'login'" icon variant="text" @click="startEdit('login')"><v-icon>mdi-pencil</v-icon></v-btn>
              <template v-else>
                <v-btn icon variant="text" color="success" @click="save"><v-icon>mdi-check</v-icon></v-btn>
                <v-btn icon variant="text" color="error" @click="cancelEdit"><v-icon>mdi-close</v-icon></v-btn>
              </template>
            </div>
          </v-card-text>
        </v-card>

        <v-card variant="outlined">
          <v-card-text>
            <div class="d-flex align-center">
              <div class="flex-grow-1">
                <div class="text-caption text-grey">Password</div>
                <template v-if="editing !== 'password'">
                  <div class="text-body-1">••••••••</div>
                </template>
                <v-text-field
                  v-else
                  v-model="temp"
                  variant="outlined"
                  density="compact"
                  hide-details
                  type="password"
                  autofocus
                  @keyup.enter="save"
                  @keyup.esc="cancelEdit"
                />
              </div>
              <v-btn v-if="editing !== 'password'" variant="text" prepend-icon="mdi-lock-reset" @click="startEdit('password')">Change</v-btn>
              <template v-else>
                <v-btn icon variant="text" color="success" @click="save"><v-icon>mdi-check</v-icon></v-btn>
                <v-btn icon variant="text" color="error" @click="cancelEdit"><v-icon>mdi-close</v-icon></v-btn>
              </template>
            </div>
          </v-card-text>
        </v-card>
      </v-form>
    </v-card>
  </v-container>
</template>

<style scoped>
.v-card { border-radius: 8px; }
.v-card-text { padding: 16px; }
.text-caption { font-size: 0.75rem; line-height: 1.25; opacity: 0.7; }
</style>

<script setup>
import { ref } from 'vue';

const user = ref({
  name: 'Иван Иванов',
  login: 'ivanov',
  email: 'ivanov@example.com',
  phone: '+7 (999) 123-45-67'
});

const editField = ref(null);
const tempValue = ref('');

const startEditing = (field) => {
  editField.value = field;
  tempValue.value = user.value[field];
};

const saveField = (field) => {
  user.value[field] = tempValue.value;
  editField.value = null;
};

const cancelEdit = () => {
  editField.value = null;
};
</script>

<template>
  <v-container class="py-8">
    <v-card class="pa-6">
      <v-card-title class="text-h5 mb-6">Личные данные</v-card-title>
      
      <v-divider class="mb-6"></v-divider>
      
      <v-form>
        <v-card variant="outlined" class="mb-4">
          <v-card-text>
            <div class="d-flex align-center">
              <div class="flex-grow-1">
                <div class="text-caption text-grey">ФИО</div>
                <template v-if="editField !== 'name'">
                  <div class="text-body-1">{{ user.name }}</div>
                </template>
                <v-text-field
                  v-else
                  v-model="tempValue"
                  variant="outlined"
                  density="compact"
                  hide-details
                  autofocus
                  @keyup.enter="saveField('name')"
                  @keyup.esc="cancelEdit"
                ></v-text-field>
              </div>
              <v-btn
                v-if="editField !== 'name'"
                icon
                variant="text"
                @click="startEditing('name')"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <template v-else>
                <v-btn
                  icon
                  variant="text"
                  color="success"
                  @click="saveField('name')"
                >
                  <v-icon>mdi-check</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="text"
                  color="error"
                  @click="cancelEdit"
                >
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </template>
            </div>
          </v-card-text>
        </v-card>

        <v-card variant="outlined" class="mb-4">
          <v-card-text>
            <div class="d-flex align-center">
              <div class="flex-grow-1">
                <div class="text-caption text-grey">Логин</div>
                <div class="text-body-1">{{ user.login }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>

        <v-card variant="outlined" class="mb-4">
          <v-card-text>
            <div class="d-flex align-center">
              <div class="flex-grow-1">
                <div class="text-caption text-grey">Email</div>
                <template v-if="editField !== 'email'">
                  <div class="text-body-1">{{ user.email }}</div>
                </template>
                <v-text-field
                  v-else
                  v-model="tempValue"
                  variant="outlined"
                  density="compact"
                  type="email"
                  hide-details
                  autofocus
                  @keyup.enter="saveField('email')"
                  @keyup.esc="cancelEdit"
                ></v-text-field>
              </div>
              <v-btn
                v-if="editField !== 'email'"
                icon
                variant="text"
                @click="startEditing('email')"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <template v-else>
                <v-btn
                  icon
                  variant="text"
                  color="success"
                  @click="saveField('email')"
                >
                  <v-icon>mdi-check</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="text"
                  color="error"
                  @click="cancelEdit"
                >
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </template>
            </div>
          </v-card-text>
        </v-card>

        <v-card variant="outlined" class="mb-4">
          <v-card-text>
            <div class="d-flex align-center">
              <div class="flex-grow-1">
                <div class="text-caption text-grey">Пароль</div>
                <div class="text-body-1">••••••••</div>
              </div>
              <v-btn
                variant="text"
                color="primary"
                prepend-icon="mdi-lock-reset"
                @click="$router.push('/change-password')"
              >
                Изменить
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-form>
    </v-card>
  </v-container>
</template>

<style scoped>
.v-card {
  border-radius: 8px;
}

.v-card-text {
  padding: 16px;
}

.text-caption {
  font-size: 0.75rem;
  line-height: 1.25;
  opacity: 0.7;
}
</style>

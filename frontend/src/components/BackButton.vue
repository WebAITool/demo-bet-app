<script setup>
import { useRouter } from 'vue-router'
import { computed } from 'vue'

const props = defineProps({
  fallbackTo: { type: [Object, String], default: null },
  label: { type: String, default: 'Назад' },
  color: { type: String, default: 'default' },
  variant: { type: String, default: 'text' },
  size: { type: String, default: 'small' },
})

const router = useRouter()
const canGoBack = computed(() => window.history.length > 1)

const goBack = () => {
  if (canGoBack.value) {
    router.back()
  } else if (props.fallbackTo) {
    router.replace(props.fallbackTo)
  } else {
    router.replace({ name: 'EventsList' })
  }
}
</script>

<template>
  <v-btn :variant="variant" :color="color" :size="size" prepend-icon="mdi-arrow-left" @click="goBack">
    {{ label }}
  </v-btn>
</template>

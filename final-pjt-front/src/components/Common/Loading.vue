<template>
  <div v-if="isLoading" class="overlay">
    <div class="spinner"></div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  isLoading: {
    type: Boolean,
    required: true,
  },
});
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 스피너가 다른 요소 위에 표시되도록 설정 */
}

.spinner {
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid white;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>

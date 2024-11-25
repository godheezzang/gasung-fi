<template>
  <div class="chatbot-message">
    <div class="bubble">{{ typedText }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const props = defineProps({
  text: {
    type: String,
    required: true,
  },
});

const typedText = ref("");
let i = 0;

const viewText = () => {
  if (i < props.text.length) {
    typedText.value += props.text.charAt(i);
    i++;
    setTimeout(viewText, 30); // 글자 추가 간격
  }
};

onMounted(() => {
  viewText(); // 컴포넌트가 마운트될 때 타이핑 효과 시작
});
</script>

<style scoped>
.bubble {
  display: inline-block;
  padding: 10px;
  border-radius: 20px;
  background-color: #e9e9eb;
  color: black;
}
</style>

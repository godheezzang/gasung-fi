<template>
  <textarea placeholder="내용을 작성해 주세요." :value="modelValue" @input="onInput" style="overflow: hidden; resize: none"></textarea>
</template>

<script setup>
import { ref, defineProps, defineEmits, onMounted } from "vue";

const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  id: String,
  placeholder: String,
});

const emit = defineEmits(["update:modelValue"]);

const onInput = (event) => {
  const value = event.target.value;
  emit("update:modelValue", value); // v-model과 연동
  adjustHeight(event.target); // 텍스트 영역 높이 조절
};

const adjustHeight = (textarea) => {
  textarea.style.height = "auto"; // 높이 초기화
  textarea.style.height = textarea.scrollHeight + "px"; // 새 높이 설정
};

// 초기 높이 조정
const adjustHeightOnMount = () => {
  const textarea = document.querySelector("textarea");
  if (textarea) {
    adjustHeight(textarea);
  }
};

onMounted(adjustHeightOnMount);
</script>

<style scoped>
textarea {
  width: 100%; /* 너비를 100%로 설정 */
  padding: 10px; /* 패딩 추가 */
  border: 1px solid #ccc; /* 테두리 스타일 */
  border-radius: 4px; /* 모서리 둥글게 */
  font-size: 16px; /* 글자 크기 */
  box-sizing: border-box; /* 패딩과 테두리를 포함한 너비 계산 */
}
</style>

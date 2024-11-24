<template>
  <div class="modal" v-if="isVisible">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h1>상품 그래프</h1>
      {{ productDetail.fin_prdt_nm }}
      <!-- 추가적인 그래프 관련 내용 -->
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";
// TODO: 그래프 그리기
const props = defineProps({
  productDetail: Object,
  isVisible: Boolean,
  closeModal: Function,
});
</script>

<style scoped>
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
}

.close {
  cursor: pointer;
  float: right;
}
</style>

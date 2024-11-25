<template>
  <RouterLink
    :to="{
      name: 'product_detail',
      params: { product_id: item.fin_prdt_cd },
      query: { product_type: productType },
    }"
  >
    <div class="product-card">
      <p>공시 제출월: {{ item.dcls_month }}</p>
      <p>금융 회사명: {{ item.kor_co_nm }}</p>
      <p>상품명: {{ item.fin_prdt_nm }}</p>
      <!-- <ul>
        <li v-for="option in item.options" :key="option.installment_savings_option_id || option.deposit_option_id">
          <p>저축 금리 유형: {{ option.intr_rate_type }}</p>
          <p>저축 금리 유형명: {{ option.intr_rate_type_nm }}</p>
          <p>저축 기간: {{ option.save_trm }}</p>
          <p>저축 금리: {{ option.intr_rate }}</p>
          <p>최고 우대 금리: {{ option.intr_rate2 }}</p>
        </li>
      </ul> -->
    </div>
  </RouterLink>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  item: Object,
});

const productType = ref("");

watch(
  () => props.item,
  (newItem) => {
    if (newItem) {
      if (newItem.installment_savings_id) {
        productType.value = "saving";
      } else if (newItem.deposit_id) {
        productType.value = "deposit";
      } else {
        productType.value = null;
      }
    }
  },
  { immediate: true }
);
</script>

<style scoped></style>

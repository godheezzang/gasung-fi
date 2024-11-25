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

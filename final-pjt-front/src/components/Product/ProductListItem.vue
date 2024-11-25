<template>
  <RouterLink
    :to="{
      name: 'product_detail',
      params: { product_id: item.fin_prdt_cd },
      query: { product_type: productType },
    }"
  >
    {{ item }}
    <div class="product-card">
      <p>{{ item.kor_co_nm }}</p>
      <p>{{ item.fin_prdt_nm }}</p>
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
      if (newItem.id) {
        productType.value = "saving";
      } else if (newItem.id) {
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

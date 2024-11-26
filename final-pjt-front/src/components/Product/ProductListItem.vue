<template>
  <RouterLink
    :to="{
      name: 'product_detail',
      params: { product_id: item.fin_prdt_cd },
      query: { product_type: productType },
    }"
  >
    <!-- {{ item }} -->
    <div class="product-card">
      <p class="product-bank">{{ item.kor_co_nm }}</p>
      <p class="product-name">{{ item.fin_prdt_nm }}</p>
    </div>
  </RouterLink>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

const props = defineProps({
  item: Object,
});

const route = useRoute();
const path = route.path;
const productType = path.split("/")[2];
// console.log(productType);

// watch(
//   () => props.item,
//   (newItem) => {
//     if (newItem) {
//       if (newItem.id) {
//         // console.log(newItem);
//         productType.value = "saving";
//       } else if (newItem.id) {
//         productType.value = "deposit";
//       } else {
//         productType.value = null;
//       }
//     }
//   },
//   { immediate: true }
// );
</script>

<style scoped></style>

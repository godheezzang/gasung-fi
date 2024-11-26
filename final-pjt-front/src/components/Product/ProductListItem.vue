<template>
  <RouterLink
    :to="{
      name: 'product_detail',
      params: { product_id: item.fin_prdt_cd },
      query: { product_type: productType },
    }"
  >
    <div class="product-card">
      <div class="product-card-title">
        <img :src="imgPath" alt="은행 이미지" class="bank-img" />
        <p class="product-bank">{{ item.kor_co_nm }}</p>
      </div>
      <p class="product-name">{{ item.fin_prdt_nm }}</p>
    </div>
  </RouterLink>
</template>

<script setup>
import { useBankStore } from "@/stores/bank";
import { useRoute } from "vue-router";

const props = defineProps({
  item: Object,
});

const route = useRoute();
const path = route.path;
const productType = path.split("/")[2];
const bankStore = useBankStore();
const bankName = props.item.kor_co_nm;
const imgPath = bankStore.bankImage[bankName];
</script>

<style scoped>
.product-card-title {
  display: flex;
  justify-content: center;
  align-items: center;
}

.product-bank {
  font-weight: var(--font-weight-medium);
}

.bank-img {
  width: 2.5rem;
  border-radius: 50%;
  margin-right: 1rem;
}
</style>

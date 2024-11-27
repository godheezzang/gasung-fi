<template>
  <!-- {{ product }} -->
  <RouterLink
    :to="{
      name: 'product_detail',
      params: { product_id: product.fin_prdt_cd },
    }"
  >
    <div class="product-card">
      <p class="product-name">{{ product.fin_prdt_nm }}</p>
      <div class="product-bank">
        <img :src="imgPath" alt="은행 이미지" class="product-img" />
        <p>{{ product.kor_co_nm }}</p>
      </div>
      <div class="recommend-desc">
        <p class="product-type" :class="{ deposit: isDeposit }">
          {{ product.product_type }}
        </p>
        <p>같이 찜한 사용자 수: {{ product.count }}명</p>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import { ref, watch } from "vue";
import { RouterLink } from "vue-router";
import { useBankStore } from "@/stores/bank";

const props = defineProps({
  product: Object,
});

const bankStore = useBankStore();
const bankName = props.product.kor_co_nm;
const imgPath = bankStore.bankImage[bankName];

const isDeposit = ref(false);
// product_type이 변경될 때마다 isDeposit을 업데이트
watch(
  () => props.product.product_type,
  (newType) => {
    isDeposit.value = newType === "정기 예금";
  }
);

isDeposit.value = props.product.product_type === "정기 예금";
console.log(isDeposit.value);

// count: 이 상품을 가입한 사람들(비슷한 조건)의 수
// 비슷한 사람을 찾는 조건: 나이 +- 5살, 연봉 +- 1000만원, 자산 +- 500만원
</script>

<style scoped>
.product-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.recommend-desc {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 70%;
  align-items: center;
}

.product-type {
  background-color: var(--color-primary-blue);
  width: fit-content;
  color: var(--color-white);
  padding: 0.3rem 0.5rem;
  border-radius: 5px;
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-medium);
  margin-bottom: 1rem;
}

.deposit {
  background-color: var(--color-primary-beige);
  color: var(--color-black);
  font-weight: var(--font-weight-bold);
}

.product-img {
  width: 3.5rem;
  margin-right: 1rem;
  margin-left: -3rem;
}

.product-bank {
  display: flex;
  margin: 0 auto;
  align-items: center;
  justify-content: center;
}
</style>

<template>
  <div>
    <!-- {{ product }} -->
    <p>상품명: {{ product.fin_prdt_nm }}</p>
    <p>상품 타입: {{ product.product_type }}</p>
    <p>은행: {{ product.kor_co_nm }}</p>
    <p>이 상품을 가입한 사람들의 수: {{ product.count }}명</p>
  </div>
</template>

<script setup>
const props = defineProps({
  product: Object,
});

// count: 이 상품을 가입한 사람들(비슷한 조건)의 수
// 비슷한 사람을 찾는 조건: 나이 +- 5살, 연봉 +- 1000만원, 자산 +- 500만원
</script>

<style scoped></style>

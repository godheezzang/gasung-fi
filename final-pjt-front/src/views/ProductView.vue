<template>
  <div class="main">
    <div class="main-nav">
      <RouterLink :to="{ name: 'product_deposits' }">예금 상품 목록</RouterLink>
      <RouterLink :to="{ name: 'product_savings' }">적금 상품 목록</RouterLink>
      <RouterLink :to="{ name: 'product_recommend' }"
        >상품 추천 받기</RouterLink
      >
    </div>
    <RouterView />
  </div>
</template>

<script setup>
import DepositList from "@/components/Product/DepositList.vue";
import SavingList from "@/components/Product/SavingList.vue";
import { RouterLink, RouterView } from "vue-router";
</script>

<style scoped></style>

<template>
  <div>
    <RouterLink :to="{ name: 'product_deposits' }">예금 상품 목록</RouterLink>
    <RouterLink :to="{ name: 'product_savings' }">적금 상품 목록</RouterLink>
  </div>
  <RouterView />
</template>

<script setup>
import DepositList from "@/components/Product/DepositList.vue";
import SavingList from "@/components/Product/SavingList.vue";
import { RouterLink, RouterView } from "vue-router";
</script>

<style scoped></style>

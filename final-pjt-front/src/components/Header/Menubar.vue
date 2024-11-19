<template>
  <div>
    <nav>
      <RouterLink :to="{ name: 'home' }">메인</RouterLink>
      <RouterLink :to="{ name: 'products' }">상품</RouterLink>
      <RouterLink :to="{ name: 'exchange_rate' }">환율</RouterLink>
      <RouterLink :to="{ name: 'search_bank' }">은행 검색</RouterLink>
      <RouterLink :to="{ name: 'community' }">커뮤니티</RouterLink>
    </nav>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped></style>

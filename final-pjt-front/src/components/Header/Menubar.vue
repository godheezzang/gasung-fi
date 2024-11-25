<template>
  <div class="menu-parent">
    <nav class="menu-container">
      <RouterLink :to="{ name: 'home' }">메인</RouterLink>
      <RouterLink :to="{ name: 'products' }">상품</RouterLink>
      <RouterLink :to="{ name: 'exchange_rate' }">환율</RouterLink>
      <RouterLink :to="{ name: 'search_bank' }">은행 검색</RouterLink>
      <RouterLink :to="{ name: 'community' }">커뮤니티</RouterLink>
      <RouterLink :to="{ name: 'qna' }">Q&A</RouterLink>
    </nav>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
.menu-container {
  margin: 0 auto;
  width: fit-content;
  display: flex;
  gap: 2rem;
  box-shadow: inset 0 0 20px purple;
  font-size: var(--font-size-large);
  font-weight: var(--font-weight-medium);
}

.menu-parent {
  /* box-shadow: inset 0 0 20px tan; */
  padding: 5rem 0;
  border-bottom: 1px solid var(--color-gray-04);
}
</style>

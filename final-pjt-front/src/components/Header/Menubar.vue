<template>
  <div class="menu-parent">
    <nav class="menu-container">
      <RouterLink :to="{ name: 'home' }">메인</RouterLink>
      <RouterLink :to="{ name: 'product_deposits' }">상품</RouterLink>
      <RouterLink :to="{ name: 'exchange_rate_home' }">환율</RouterLink>
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
  /* box-shadow: inset 0 0 20px purple; */
  font-size: var(--font-size-large);
  font-weight: var(--font-weight-regular);
}

.menu-container .router-link-active,
.menu-container .router-link-exact-active {
  font-weight: var(--font-weight-bold);
  border-bottom: 4px solid var(--color-primary-blue);
}

.menu-parent {
  /* box-shadow: inset 0 0 20px tan; */
  padding: 2rem 0 1rem 0;
  border-bottom: 1px solid var(--color-gray-04);
}

.menu-parent a {
  transition: border-bottom 0.1s ease;
}

.menu-parent a:hover {
  border-bottom: 4px solid var(--color-primary-blue);
}
</style>

<template>
  <div>
    <RouterLink :to="{ name: 'my_profile' }">내 정보 수정</RouterLink>
    <RouterLink :to="{ name: 'my_products' }">내 상품 확인</RouterLink>
    <RouterLink :to="{ name: 'password_verification' }">비밀번호 수정</RouterLink>
  </div>
  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<style scoped></style>

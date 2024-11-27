<template>
  <div v-if="!isLoggedIn" class="nav-container">
    <RouterLink :to="{ name: 'login' }">로그인</RouterLink>
    <RouterLink :to="{ name: 'signup' }">회원가입</RouterLink>
  </div>
  <div v-if="isLoggedIn" class="nav-container">
    <RouterLink :to="{ name: 'my_profile' }">프로필</RouterLink>
    <RouterLink :to="{ name: 'my_products' }">내 상품</RouterLink>
    <Button
      :onClick="handleLogout"
      content="로그아웃"
      ariaLabel="로그아웃"
      customClass="small-btn"
    ></Button>
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import { useUserStore } from "@/stores/user";
import { computed } from "vue";
import { RouterLink } from "vue-router";

const userStore = useUserStore();
const isLoggedIn = computed(() => userStore.$state.isLoggedIn);

const handleLogout = () => {
  userStore.logout();
};
</script>

<style scoped>
.nav-container {
  /* box-shadow: inset 0 0 20px red; */
  width: fit-content;
  margin-left: auto;
  display: flex;
  gap: 0.5rem;
  font-weight: var(--font-weight-regular);
  font-size: var(--font-size-small);
  align-items: center;
  margin-top: 1rem;
}
</style>

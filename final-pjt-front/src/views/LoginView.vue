<template>
  <div class="main-container">
    <h1 class="login-title">로그인</h1>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="login-input">
        <label for="email" class="login-label">이메일</label>
        <input type="text" id="email" class="user-input" v-model="emailInput" placeholder="gasung_fi@example.com" />
        <label for="password" class="login-label">비밀번호</label>
        <input type="password" id="password" class="user-input" v-model="pwInput" placeholder="8자 이상의 비밀번호를 입력해 주세요." />
      </div>
      <p class="err-msg" v-if="!isValid">아이디와 비밀번호를 다시 확인해 주세요.</p>

      <Button content="로그인" ariaLabel="로그인" type="submit"></Button>
      <div class="login-desc">
        <p>회원이 아니신가요?</p>
        <RouterLink :to="{ name: 'signup' }">회원가입하기</RouterLink>
      </div>
    </form>
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import { useUserStore } from "@/stores/user";
import { ref } from "vue";
import axiosInstance from "@/plugins/axios";
import { useRouter } from "vue-router";

const store = useUserStore();
const router = useRouter();
const emailInput = ref("");
const pwInput = ref("");
const isValid = ref(true);

const handleLogin = async () => {
  const userData = {
    email: emailInput.value,
    password: pwInput.value,
  };
  const errMsg = store.login(userData);
  if (errMsg) {
    isValid.value = false;
  }
};
</script>

<style scoped>
.main-container {
  height: 84vh;
  margin: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 5rem;
}
</style>

<template>
  <div>
    <h1>로그인</h1>
    <form @submit.prevent="handleLogin">
      <label for="email">이메일</label>
      <input type="text" id="email" class="user-input" v-model="emailInput" placeholder="이메일을 입력해 주세요." />
      <label for="password">비밀번호</label>
      <input type="password" id="password" class="user-input" v-model="pwInput" placeholder="비밀번호를 입력해 주세요." />
      <Button content="로그인" ariaLabel="로그인" type="submit"></Button>
      <p v-if="!isValid">아이디와 비밀번호를 다시 확인해 주세요.</p>
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

<style scoped></style>

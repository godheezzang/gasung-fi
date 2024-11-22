<template>
  <div>
    <h1>회원가입</h1>
    <form @submit.prevent="handleSignup">
      <label for="email">이메일</label>
      <input type="text" id="email" v-model="emailInput" class="user-input" />
      <label for="username">이름</label>
      <input type="text" id="username" v-model="nameInput" class="user-input" />
      <label for="password1">비밀번호</label>
      <input
        type="password"
        id="password1"
        v-model="firstPwInput"
        class="user-input"
      />
      <label for="password2">비밀번호 확인</label>
      <input
        type="password"
        id="password2"
        v-model="secondPwInput"
        class="user-input"
      />
      <Button content="회원가입" type="submit" ariaLabel="회원가입" />
    </form>
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import axios from "axios";
import { ref } from "vue";

const emailInput = ref("");
const nameInput = ref("");
const firstPwInput = ref("");
const secondPwInput = ref("");

const handleSignup = async () => {
  try {
    if (firstPwInput.value !== secondPwInput.value) {
      alert("비밀번호 일치하지 않음");
    }
    const userData = {
      email: emailInput.value,
      username: nameInput.value,
      password1: firstPwInput.value,
      password2: secondPwInput.value,
    };
    const response = await axios.post(
      `${import.meta.env.VITE_BASE_URL}/accounts/signup/`,
      userData
    );

    console.log(response);

    if (response.status === 201) {
      console.log(response.data);
    }
  } catch (err) {
    throw new Error(err);
  }
};
</script>

<style scoped></style>

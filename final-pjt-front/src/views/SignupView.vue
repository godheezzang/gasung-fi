<template>
  <div class="main-container">
    <h1 class="login-title">회원가입</h1>
    <form @submit.prevent="handleSignup" class="login-form">
      <div class="login-input">
        <label for="email">이메일</label>
        <input type="text" id="email" v-model="emailInput" class="user-input" placeholder="gasung_fi@example.com" />
        <p class="err-msg" v-if="isEmailDuplicate">이 이메일은 이미 사용 중입니다.</p>
        <p class="err-msg" v-if="isEmailInvalid">정확한 이메일을 입력해 주세요.</p>
        <p class="err-msg" v-if="emailErrors.length">{{ emailErrors[0] }}</p>
        <label for="username">이름</label>
        <input type="text" id="username" v-model="nameInput" class="user-input" placeholder="김싸피" />
        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model="firstPwInput" class="user-input" placeholder="8자 이상의 특수문자가 포함된 비밀번호를 입력해 주세요." />
        <p class="err-msg" v-if="firstPwInput.length < 8 && firstPwInput.length > 1">비밀번호는 8자 이상이어야 합니다.</p>
        <p class="err-msg" v-if="isPwCommon">안전한 비밀번호를 사용해 주세요.</p>
        <p class="err-msg" v-if="passwordErrors.length">{{ passwordErrors[0] }}</p>
        <label for="password2">비밀번호 확인</label>
        <input type="password" id="password2" v-model="secondPwInput" class="user-input" placeholder="위 비밀번호와 동일한 비밀번호를 입력해 주세요." />
        <p class="err-msg" v-if="firstPwInput !== secondPwInput">비밀번호가 일치하지 않습니다.</p>
      </div>

      <Button content="회원가입" type="submit" ariaLabel="회원가입" customClass="default-btn" />
    </form>
  </div>
</template>

// TODO: 회원가입 유효성 검사 로직 수정
<script setup>
import Button from "@/components/Common/Button.vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useUserStore();

const emailInput = ref("");
const nameInput = ref("");
const firstPwInput = ref("");
const secondPwInput = ref("");

const isEmailDuplicate = ref(false);
const isEmailInvalid = ref(false);
const isPwCommon = ref(false);

const emailErrors = ref([]);
const passwordErrors = ref([]);

const handleSignup = async () => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(emailInput.value)) {
    isEmailInvalid.value = true;
    return;
  }

  if (firstPwInput.value !== secondPwInput.value) {
    return;
  }

  const commonPasswords = ["123456", "password", "12345678", "11111111"];
  if (commonPasswords.includes(firstPwInput.value)) {
    isPwCommon.value = true;
    return;
  }

  const data = {
    email: emailInput.value,
    username: nameInput.value,
    password1: firstPwInput.value,
    password2: secondPwInput.value,
  };
  const errResponse = await store.signup(data);
  if (errResponse) {
    if (errResponse.email) {
      emailErrors.value = errResponse.email;
    }

    if (errResponse.password1) {
      passwordErrors.value = errResponse.password1;
    }

    if (errResponse.non_field_errors) {
      passwordErrors.value = errResponse.non_field_errors;
    }
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

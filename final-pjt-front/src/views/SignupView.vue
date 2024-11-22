<template>
  <div>
    <h1>회원가입</h1>
    <form @submit.prevent="handleSignup">
      <div>
        <label for="email">이메일</label>
        <input
          type="text"
          id="email"
          v-model="emailInput"
          class="user-input"
          placeholder="예) gasung@site.com"
        />
        <span v-if="isEmailDuplicate">이 이메일은 이미 사용 중입니다.</span>
        <span v-if="isEmailInvalid">정확한 이메일을 입력해 주세요.</span>
      </div>
      <div>
        <label for="username">이름</label>
        <input
          type="text"
          id="username"
          v-model="nameInput"
          class="user-input"
          placeholder="예) 김가성"
        />
      </div>
      <div>
        <label for="password1">비밀번호</label>
        <input
          type="password"
          id="password1"
          v-model="firstPwInput"
          class="user-input"
          placeholder="8자 이상, 특수문자를 포함"
        />
        <span v-if="firstPwInput < 8">비밀번호는 8자 이상이어야 합니다.</span>
        <span v-if="isPwCommon">안전한 비밀번호를 사용해 주세요.</span>
      </div>
      <div>
        <label for="password2">비밀번호 확인</label>
        <input
          type="password"
          id="password2"
          v-model="secondPwInput"
          class="user-input"
        />
        <span v-if="firstPwInput !== secondPwInput"
          >비밀번호가 일치하지 않습니다.</span
        >
      </div>

      <Button
        content="회원가입"
        type="submit"
        ariaLabel="회원가입"
        customClass="disabled-btn"
      />

      <Button
        content="회원가입"
        type="submit"
        ariaLabel="회원가입"
        customClass="default-btn"
      />
    </form>
  </div>
</template>

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

const emailDuplicateMsg = "이 이메일은 이미 사용 중입니다.";
const emailInvalidMsg = "Enter a valid email address.";
const pwCommonMsg = "This password is too common.";
const pwNumericMsg = "This password is entirely numeric.";

const isEmailDuplicate = ref("");
const isEmailInvalid = ref("");

const isPwCommon = ref("");

const handleSignup = async () => {
  try {
    if (firstPwInput.value.length < 8) {
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

    if (response.status === 201) {
      // console.log(response.data);
      const userToken = response.data.key;
      store.token = userToken;
      router.push({ name: "home" });
    }
  } catch (err) {
    console.error(err);
    // console.log(err.response.data.email);
    errData = err.response?.data;
    const emailErrors = err.response?.data?.email;
    const pw1Erors = err.response?.data?.password1;
    if (errData.email[0] === emailDuplicateMsg) {
      isEmailDuplicate.value = true;
    }

    if (errData.email[0] === emailInvalidMsg) {
      isEmailInvalid.value = true;
    }

    pw1Erors.forEach((err) => {
      if (err.includes("too common")) {
        isPwCommon.value = true;
      }
    });
  }
};
</script>

<style scoped></style>

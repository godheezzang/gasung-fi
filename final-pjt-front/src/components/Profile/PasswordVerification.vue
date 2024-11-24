<template>
  <div>
    <h1>비밀번호 확인</h1>
    <p>현재 비밀번호를 입력해주세요.</p>

    <form @submit.prevent="verifyPassword">
      <input type="password" v-model="pwInput" />
      <Button content="확인" type="submit" ariaLabel="비밀번호 확인" />
    </form>
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import { useUserStore } from "@/stores/user";
import { ref } from "vue";
import { useRouter } from "vue-router";

const store = useUserStore();
const pwInput = ref("");
const router = useRouter();

const verifyPassword = () => {
  if (pwInput.value === store.password) {
    router.push({ name: "change_password" });
  } else {
    alert("비밀번호가 일치하지 않습니다.");
  }
};
</script>

<style scoped></style>

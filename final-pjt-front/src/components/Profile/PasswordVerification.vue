<template>
  <div class="pw-container">
    <div class="pw-wrap">
      <h1 class="pw-title">비밀번호 확인</h1>
      <p class="pw-desc">현재 비밀번호를 입력해주세요.</p>

      <form @submit.prevent="verifyPassword" class="pw-form">
        <input
          type="password"
          v-model="pwInput"
          class="user-input"
          placeholder="현재 사용 중인 비밀번호를 입력하세요."
        />
        <p class="err-msg" v-if="!isValid">
          현재 사용 중인 비밀번호와 다릅니다.
        </p>

        <Button
          content="확인"
          type="submit"
          ariaLabel="비밀번호 확인"
          class="pw-btn"
        />
      </form>
    </div>
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
const isValid = ref(true);

const verifyPassword = () => {
  if (pwInput.value === store.password) {
    router.push({ name: "change_password" });
  } else {
    isValid.value = false;
    // alert("비밀번호가 일치하지 않습니다.");
  }
};
</script>

<style scoped>
.pw-container {
  /* box-shadow: inset 0 0 20px red; */
  margin-top: 2rem;
}

.pw-wrap {
  /* box-shadow: inset 0 0 20px blue; */
  width: 50%;
  margin: 0 auto;
}

.pw-desc {
  text-align: center;
  margin: 1rem 0 2rem 0;
}

.user-input {
  border-radius: 5px;
  width: 40%;
  height: 4rem;
  text-align: center;
}

.pw-title {
  font-size: var(--font-size-extra-large);
  font-weight: var(--font-weight-medium);
  text-align: center;
}

.pw-form {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.pw-btn {
  width: 40%;
}
</style>

<template>
  <div class="change-container">
    <div class="change-wrap">
      <h1 class="change-title">비밀번호 변경</h1>
      <form @submit.prevent="handleChangePw" class="change-form">
        <div class="form-content">
          <label for="currentPw" class="form-label">현재 비밀번호</label>
          <input
            type="password"
            id="currentPw"
            v-model="currentPw"
            placeholder="현재 사용 중인 비밀번호를 입력하세요."
            class="user-input"
          />
          <p v-if="store.password !== currentPw" class="err-msg">
            현재 비밀번호가 일치하지 않습니다.
          </p>
        </div>
        <div class="form-content">
          <label for="newPw1" class="form-label">변경할 비밀번호</label>
          <input
            type="password"
            id="newPw1"
            v-model="newPw1"
            placeholder="8자 이상, 특수문자 포함"
            class="user-input"
          />
          <p v-if="currentPw === newPw1" class="err-msg">
            현재 비밀번호와 동일합니다. 다른 비밀번호를 입력하세요.
          </p>
        </div>
        <div class="form-content">
          <label for="newPw2" class="form-label">변경할 비밀번호 확인</label>
          <input
            type="password"
            id="newPw2"
            v-model="newPw2"
            class="user-input"
            placeholder="위와 동일한 비밀번호를 입력해 주세요."
          />
          <p v-if="newPw1 !== newPw2" class="err-msg">
            입력한 비밀번호가 일치하지 않습니다. 확인해 주세요.
          </p>
        </div>
        <Button
          content="비밀번호 변경"
          ariaLabel="비밀번호 변경"
          type="submit"
        />
      </form>
    </div>
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";

const store = useUserStore();
const router = useRouter();
const currentPw = ref("");
const newPw1 = ref("");
const newPw2 = ref("");

const handleChangePw = async () => {
  if (newPw1.value !== newPw2.value) {
    return;
  }

  if (currentPw.value === newPw1.value) {
    return;
  }

  if (currentPw.value !== store.password) {
    return;
  }

  try {
    const response = await axios({
      method: "post",
      url: `${import.meta.env.VITE_BASE_URL}/accounts/password/change/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
      data: {
        old_password: currentPw.value,
        new_password1: newPw1.value,
        new_password2: newPw2.value,
      },
    });
    alert("비밀번호가 변경되었습니다.");

    const data = {
      email: store.userEmail,
      password: newPw1.value,
    };

    // 다시 재로그인 시키고
    store.login(data);
    // 홈으로 리다이렉트
    router.push({ name: "home" });
  } catch (error) {
    console.error(error);
  }
};
</script>

<style scoped>
.change-container {
  /* box-shadow: inset 0 0 20px red; */
  margin-top: 2rem;
}

.change-wrap {
  /* box-shadow: inset 0 0 20px blue; */
  width: 50%;
  margin: 0 auto;
}

.user-input {
  border-radius: 5px;
  height: 4rem;
  text-align: center;
}

.change-title {
  font-size: var(--font-size-extra-large);
  font-weight: var(--font-weight-medium);
  text-align: center;
  margin-bottom: 2rem;
}

.change-form {
  /* box-shadow: inset 0 0 20px plum; */
  display: flex;
  flex-direction: column;
  width: 50%;
  margin: 0 auto;
  justify-content: center;
  gap: 2rem;
}

.form-content {
  /* box-shadow: inset 0 0 20px salmon; */
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 0.7rem;
}

.form-label {
  font-size: var(--font-size-mlarge);
  text-align: center;
  font-weight: var(--font-weight-medium);
}
</style>

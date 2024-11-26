<template>
  <div class="profile-container">
    <div class="profile-wrap">
      <form @submit.prevent="handleUpdate" class="profile-form">
        <div class="profile-required">
          <h3 class="profile-title">필수 정보</h3>
          <div class="profile-input">
            <!-- 클래스명 실화? TODO: Refactor - html 구조 수정 -->
            <div class="profile-input-type">
              <label for="email" class="profile-label">이메일</label>
              <input
                type="text"
                id="email"
                v-model="email"
                class="user-input"
              />
            </div>
            <div class="profile-input-type">
              <label for="username" class="profile-label">이름</label>
              <input
                type="text"
                id="username"
                v-model.trim="username"
                class="user-input"
              />
            </div>
            <p class="err-msg" v-if="username.length === 0">
              이름을 입력해 주세요.
            </p>
          </div>
        </div>
        <div class="profile-additional">
          <h3 class="profile-title">추가 정보</h3>
          <div class="profile-input">
            <div class="profile-input-type">
              <label for="gender" class="profile-label">성별</label>
              <select class="custom-select" id="gender" v-model="gender">
                <option value="" disabled>선택하세요</option>
                <option value="M">남자</option>
                <option value="W">여자</option>
              </select>
            </div>
            <div class="profile-input-type">
              <label for="age" class="profile-label">나이</label>
              <input
                type="number"
                id="age"
                v-model="age"
                placeholder="나이를 입력하세요."
                class="user-input"
                min="8"
              />
              세
            </div>
            <div class="profile-input-type">
              <label for="income" class="profile-label">연봉</label>
              <input
                type="text"
                id="income"
                :value="formatNumber(income)"
                @input="updateIncome"
                placeholder="연봉을 입력하세요."
                class="user-input"
              />
              (만)원
            </div>
            <p class="err-msg" v-if="Number(income) > 2147483647">
              2,147,483,647보다 큰 값은 입력하실 수 없습니다.
            </p>
            <div class="profile-input-type">
              <label for="assets" class="profile-label">자산</label>
              <input
                type="text"
                id="assets"
                :value="formatNumber(assets)"
                @input="updateAssets"
                placeholder="자산을 입력하세요."
                class="user-input"
              />
              (만)원
            </div>
            <p class="err-msg" v-if="Number(assets) >= 2147483647">
              2,147,483,647보다 큰 값은 입력하실 수 없습니다.
            </p>
          </div>
        </div>
        <div class="profile-btn">
          <Button content="정보 수정" ariaLabel="정보 수정" type="submit" />
        </div>
      </form>
    </div>
  </div>
  <Loading :isLoading="isLoading" />
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import Loading from "@/components/Common/Loading.vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { onMounted, ref } from "vue";

const store = useUserStore();
const userData = ref({});

// v-models
const email = ref("");

const username = ref("");
const gender = ref("");
const age = ref(null);
const income = ref(null);
const assets = ref(null);
const isLoading = ref(false);

// 숫자 포맷팅 함수
const formatNumber = (value) => {
  if (value === null || value === undefined) return "";
  return new Intl.NumberFormat().format(value);
};

// 입력 값 업데이트 함수
const updateIncome = (event) => {
  const value = event.target.value.replace(/,/g, ""); // 콤마 제거
  income.value = value ? Number(value) : null; // 숫자로 변환
};

const updateAssets = (event) => {
  const value = event.target.value.replace(/,/g, ""); // 콤마 제거
  assets.value = value ? Number(value) : null; // 숫자로 변환
};

// 개인정보 update 로직
const handleUpdate = async () => {
  isLoading.value = true;
  try {
    // 수정할 데이터 객체 생성
    const updatedData = {};

    // 변경된 값만 추가
    if (email.value !== userData.value.email) {
      updatedData.email = email.value;
    }
    if (username.value !== userData.value.username) {
      updatedData.username = username.value;
    }

    if (gender.value !== userData.value.gender) {
      updatedData.gender = gender.value;
    }
    if (age.value !== userData.value.age) {
      updatedData.age = age.value;
    }
    if (income.value !== userData.value.income) {
      updatedData.income = income.value;
    }
    if (assets.value !== userData.value.assets) {
      updatedData.assets = assets.value;
    }

    if (assets.value > 2147483647 || income.value > 2147483647) {
      return;
    }

    if (username.length === 0) {
      return;
    }

    const response = await axios({
      method: "put",
      url: `${import.meta.env.VITE_BASE_URL}/accounts/detail/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
      data: updatedData,
    });

    if (response.status === 200) {
      isLoading.value = false;
      alert("정보가 변경되었습니다.");
    }
  } catch (error) {
    isLoading.value = false;
    console.error(error);
  }
};
// 개인정보 fetch 로직
const fetchUserData = async () => {
  isLoading.value = true;
  try {
    const response = await axios({
      method: "get",
      url: `${import.meta.env.VITE_BASE_URL}/accounts/detail/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    // console.log(response);
    if (response.status === 200) {
      userData.value = response.data;
      console.log(userData.value);
      email.value = userData.value.email;
      username.value = userData.value.username;
      gender.value = userData.value.gender;
      age.value = userData.value.age;
      income.value = userData.value.income;
      assets.value = userData.value.assets;

      isLoading.value = true;
    }
  } catch (error) {
    isLoading.value = false;
    console.error(error);
  }
};

onMounted(async () => {
  isLoading.value = true;
  await fetchUserData();
  isLoading.value = false;
});
</script>

<style scoped>
.profile-container {
  /* box-shadow: inset 0 0 20px red; */
  width: 70%;
  margin: 0 auto;
}

.profile-wrap {
  /* box-shadow: inset 0 0 20px black; */
  margin: 0 auto;
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  /* align-items: center; */
  min-height: 63rem;
  width: 50%;
  border: 1px solid var(--color-gray-02);
  border-radius: 5px;
}

.profile-form {
  /* box-shadow: inset 0 0 20px navy; */
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 1rem 0;
}

.profile-required {
  /* box-shadow: inset 0 0 20px red; */
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-bottom: 1px solid var(--color-gray-02);
  padding: 2rem;
}

.profile-additional {
  /* box-shadow: inset 0 0 20px lime; */
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-bottom: 1px solid var(--color-gray-02);
  margin-bottom: 1rem;
  padding: 2rem;
}

.profile-btn {
  /* box-shadow: inset 0 0 20px purple; */
  flex-grow: 0;
  display: flex;
  justify-content: center;
}

.profile-title {
  font-size: var(--font-size-large);
  font-weight: var(--font-weight-bold);
}

.profile-input {
  /* box-shadow: inset 0 0 20px yellow; */
  margin: 2rem 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.profile-input-type {
  /* box-shadow: inset 0 0 20px hotpink; */
  height: 5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.profile-input-type input,
.profile-input-type select {
  flex-grow: 2;
  height: 100%;
  border-radius: 5px;
  max-width: 80%;
}

.profile-label {
  /* box-shadow: inset 0 0 20px brown; */
  font-size: var(--font-size-mlarge);
  font-weight: var(--font-weight-medium);
  flex-grow: 0.3;
  max-width: 5rem;
}

.err-msg {
  margin-left: 6rem;
}
</style>

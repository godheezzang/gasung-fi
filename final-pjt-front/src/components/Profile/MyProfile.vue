<template>
  <div>
    <h1>내 정보 수정</h1>
    <form @submit.prevent="handleUpdate">
      <div>
        <p>필수 정보</p>
        <div>
          <label for="email">이메일: </label>
          <input type="text" id="email" v-model="email" />
        </div>

        <div>
          <label for="username">이름</label>
          <input type="text" id="username" v-model="username" />
        </div>
      </div>
      <div>
        <p>추가 정보</p>
        <div>
          <label for="gender">성별</label>
          <select id="gender" v-model="gender">
            <option value="" disabled>선택하세요</option>
            <option value="M">남자</option>
            <option value="W">여자</option>
          </select>
        </div>
        <div>
          <label for="age">나이</label>
          <input type="number" id="age" v-model="age" placeholder="나이를 입력하세요." />
        </div>
        <div>
          <label for="income">연봉</label>
          <input type="text" id="income" :value="formatNumber(income)" @input="updateIncome" placeholder="연봉을 입력하세요." /> (만)원
        </div>
        <div>
          <label for="assets">자산</label>
          <input type="text" id="assets" :value="formatNumber(assets)" @input="updateAssets" placeholder="자산을 입력하세요." /> (만)원
        </div>
      </div>
      <Button content="정보 수정" ariaLabel="정보 수정" type="submit" />
    </form>
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { ref } from "vue";

const store = useUserStore();
const userData = ref({});

// v-models
const email = ref("");

const username = ref("");
const gender = ref("");
const age = ref(null);
const income = ref(null);
const assets = ref(null);

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

    const response = await axios({
      method: "put",
      url: `${import.meta.env.VITE_BASE_URL}/accounts/detail/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
      data: updatedData,
    });

    console.log(response);
  } catch (error) {
    console.error(error);
  }
};
// 개인정보 fetch 로직
const fetchUserData = async () => {
  try {
    const response = await axios({
      method: "get",
      url: `${import.meta.env.VITE_BASE_URL}/accounts/detail/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    // console.log(response);
    userData.value = response.data;
    console.log(userData.value);
    email.value = userData.value.email;
    username.value = userData.value.username;
    gender.value = userData.value.gender;
    age.value = userData.value.age;
    income.value = userData.value.income;
    assets.value = userData.value.assets;
  } catch (error) {
    console.error(error);
  }
};

fetchUserData();
</script>

<style scoped></style>

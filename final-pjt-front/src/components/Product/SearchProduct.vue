<template>
  <Loading :isLoading="isLoading" />
  <div class="select-container">
    <div class="select-box">
      <label for="bank-select">은행 선택</label>
      <select class="custom-select" id="bank-select" v-model="bankName">
        <option value="">모든 은행</option>
        <option v-for="bank in banks" :key="bank" :value="bank">
          {{ bank }}
        </option>
      </select>
    </div>
    <div class="select-box">
      <label for="term-select">가입 기간 선택</label>
      <select class="custom-select" id="term-select" v-model="saveTrm">
        <option value="">모든 기간</option>
        <option value="1">1개월</option>
        <option value="3">3개월</option>
        <option value="6">6개월</option>
        <option value="12">1년</option>
        <option value="24">2년</option>
        <option value="36">3년</option>
      </select>
    </div>

    <Button content="검색" ariaLabel="검색" :onClick="searchProducts" />
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import Loading from "@/components/Common/Loading.vue";
import { useMapStore } from "@/stores/map";
import axios from "axios";
import { ref } from "vue";

const props = defineProps({
  apiUrl: {
    type: String,
    required: true,
  },
});

const bankName = ref("");
const saveTrm = ref("");
const mapStore = useMapStore();
const banks = mapStore.banks;
const BASE_URL = import.meta.env.VITE_BASE_URL;
const emit = defineEmits();
console.log(props.apiUrl);
const isLoading = ref(false);

const searchProducts = async () => {
  isLoading.value = true;
  console.log(bankName);

  try {
    const response = await axios({
      method: "get",
      url: `${BASE_URL}/${props.apiUrl}`,
      params: {
        bank_name: bankName.value,
        save_trm: saveTrm.value,
      },
    });
    // console.log(response);

    console.log(response.data);
    emit("update:products", response.data);
    isLoading.value = false;
  } catch (error) {
    console.error(error);
    isLoading.value = false;
  }
};
</script>

<style scoped></style>

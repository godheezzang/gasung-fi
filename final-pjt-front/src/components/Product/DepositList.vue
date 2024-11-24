<template>
  <div>
    <h1>DepositList</h1>
    <div class="product-container">
      <!-- {{ deposits }} -->
      <ProductListItem v-for="deposit in deposits" :key="deposit.deposit_id" :item="deposit" />
    </div>
  </div>
</template>

<script setup>
import ProductListItem from "@/components/Product/ProductListItem.vue";
import axios from "axios";
import { onMounted, ref } from "vue";

const deposits = ref([]);
const BASE_URL = import.meta.env.VITE_BASE_URL;
const fetchDeposits = async () => {
  try {
    const response = await axios({
      method: "get",
      url: `${BASE_URL}/products/deposit/`,
    });

    // console.log(response);
    deposits.value = response?.data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(async () => {
  fetchDeposits();
});
</script>

<style scoped></style>

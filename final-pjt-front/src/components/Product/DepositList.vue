<template>
  <div>
    <h1>DepositList</h1>
    <SearchProduct @update:products="updateDeposits" apiUrl="products/deposit/search" />
    <div class="product-container">
      <!-- {{ deposits }} -->
      <ProductListItem v-for="deposit in deposits" :key="deposit.deposit_id" :item="deposit" />
    </div>
    <div v-if="deposits.length === 0">
      <p>상품 정보가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import ProductListItem from "@/components/Product/ProductListItem.vue";
import SearchProduct from "@/components/Product/SearchProduct.vue";
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

const updateDeposits = (newDeposits) => {
  deposits.value = newDeposits;
};

onMounted(async () => {
  fetchDeposits();
});
</script>

<style scoped></style>

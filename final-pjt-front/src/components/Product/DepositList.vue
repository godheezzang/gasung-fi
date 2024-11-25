<template>
  <Loading :isLoading="isLoading" />
  <div>
    <div class="product-container">
      <SearchProduct @update:products="updateDeposits" apiUrl="products/deposit/search" />
      <div class="product-list">
        <!-- {{ deposits }} -->
        <div class="product-box">
          <ProductListItem v-for="deposit in deposits" :key="deposit.id" :item="deposit" />
        </div>
        <div v-if="deposits.length === 0" class="product-box">
          <p>상품 정보가 없습니다.</p>
        </div>
        <div class="pagination">
          <button @click="prevPage" :disabled="currentPage === 1" class="previous-icon">
            <img src="@/assets/icons/arrow_forward.svg" alt="이전" />
          </button>
          <span>{{ currentPage }} / {{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages" class="next-icon">
            <img src="@/assets/icons/arrow_forward.svg" alt="다음" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Loading from "@/components/Common/Loading.vue";
import ProductListItem from "@/components/Product/ProductListItem.vue";
import SearchProduct from "@/components/Product/SearchProduct.vue";
import axios from "axios";
import { onMounted, ref } from "vue";

const deposits = ref([]);
const BASE_URL = import.meta.env.VITE_BASE_URL;
const currentPage = ref(1);
const totalPages = ref(0);
const productsPerPage = 12;
const isLoading = ref(true);

const fetchDeposits = async (page = 1) => {
  try {
    const response = await axios({
      method: "get",
      url: `${BASE_URL}/products/deposit/`,
      params: {
        page,
      },
    });

    console.log(response);
    deposits.value = response?.data.results;
    totalPages.value = Math.ceil(response.data.count / productsPerPage);
    isLoading.value = false;
  } catch (error) {
    console.error(error);
  }
};

const updateDeposits = (newDeposits) => {
  deposits.value = newDeposits;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    fetchDeposits(currentPage.value);
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    fetchDeposits(currentPage.value);
  }
};

onMounted(async () => {
  await fetchDeposits(currentPage.value);
});
</script>

<style scoped></style>

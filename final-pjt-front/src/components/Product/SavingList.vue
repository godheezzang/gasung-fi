<template>
  <Loading :isLoading="isLoading" />
  <div>
    <div class="product-container">
      <SearchProduct apiUrl="products/installment_savings/search" @update:products="updateSavings" />
      <div class="product-list">
        <!-- {{ savings }} -->
        <div class="product-box">
          <ProductListItem v-for="saving in savings" :key="saving.id" :item="saving" />
        </div>
        <div v-if="savings.length === 0" class="product-box">
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

const savings = ref([]);
const BASE_URL = import.meta.env.VITE_BASE_URL;
const currentPage = ref(1);
const totalPages = ref(0);
const productPerPage = 12;
const isLoading = ref(true);

const fetchSavings = async (page = 1) => {
  try {
    const response = await axios({
      method: "get",
      url: `${BASE_URL}/products/installment_savings/`,
      params: {
        page,
      },
    });

    // console.log(response);
    savings.value = response?.data.results;
    totalPages.value = Math.ceil(response.data.count / productPerPage);
    isLoading.value = false;
  } catch (error) {
    console.error(error);
  }
};

const updateSavings = (newSavings) => {
  savings.value = newSavings; // 검색 결과로 savings 업데이트
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    fetchSavings(currentPage.value);
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    fetchSavings(currentPage.value);
  }
};

onMounted(async () => {
  await fetchSavings(currentPage.value);
});
</script>

<style scoped></style>

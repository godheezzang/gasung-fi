<template>
  <div class="product-container">
    <SearchProduct
      apiUrl="products/installment_savings/search"
      @update:products="updateSavings"
    />
    <div class="product-list">
      <!-- {{ savings }} -->
      <ProductListItem
        v-for="saving in savings"
        :key="saving.installment_savings_id"
        :item="saving"
      />
      <div v-if="savings.length === 0">
        <p>상품 정보가 없습니다.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import ProductListItem from "@/components/Product/ProductListItem.vue";
import SearchProduct from "@/components/Product/SearchProduct.vue";
import axios from "axios";
import { onMounted, ref } from "vue";

const savings = ref([]);
const BASE_URL = import.meta.env.VITE_BASE_URL;
const fetchSavings = async () => {
  try {
    const response = await axios({
      method: "get",
      url: `${BASE_URL}/products/installment_savings/`,
    });

    // console.log(response);
    savings.value = response?.data;
  } catch (error) {
    console.error(error);
  }
};

const updateSavings = (newSavings) => {
  savings.value = newSavings; // 검색 결과로 savings 업데이트
};

onMounted(async () => {
  fetchSavings();
});
</script>

<style scoped></style>

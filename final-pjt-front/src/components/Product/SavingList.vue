<template>
  <div>
    <h1>SavingList</h1>
    <div class="product-container">
      <!-- {{ savings }} -->
      <ProductListItem v-for="saving in savings" :key="saving.installment_savings_id" :item="saving" />
    </div>
  </div>
</template>

<script setup>
import ProductListItem from "@/components/Product/ProductListItem.vue";
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

onMounted(async () => {
  fetchSavings();
});
</script>

<style scoped></style>

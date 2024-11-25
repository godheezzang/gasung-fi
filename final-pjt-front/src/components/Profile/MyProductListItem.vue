<template>
  <div @click="openModal" class="product-card">
    <p>상품명: {{ product.fin_prdt_nm }}</p>
    <p>상품 타입: {{ product.product_type }}</p>
    <p>은행: {{ product.kor_co_nm }}</p>
    <p>찜한 날짜: {{ formatDate(product.created_at) }}</p>
  </div>
  <MyProductGraph :productDetail="productDetail" :isVisible="isVisible" :closeModal="closeModal" />
</template>

<script setup>
import MyProductGraph from "@/components/Profile/MyProductGraph.vue";
import axios from "axios";
import { onMounted, ref } from "vue";

const props = defineProps({
  product: Object,
});

const BASE_URL = import.meta.env.VITE_BASE_URL;
const finPrdtCd = props.product.fin_prdt_cd;
const productDetail = ref({});
const isVisible = ref(false);

const openModal = () => {
  isVisible.value = true;
};

const closeModal = () => {
  isVisible.value = false;
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0"); // 월은 0부터 시작하므로 +1
  const day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
};

// productType에 따라 요청 url 선택하는 로직
const getUrl = () => {
  return props.product.product_type === "정기 적금" ? `${BASE_URL}/products/installment_savings/${finPrdtCd}/` : `${BASE_URL}/products/deposit/${finPrdtCd}/`;
};

const fetchProductData = async () => {
  const url = getUrl();
  try {
    const response = await axios({
      method: "get",
      url,
    });

    productDetail.value = response.data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(async () => {
  fetchProductData();
});
</script>

<style scoped></style>

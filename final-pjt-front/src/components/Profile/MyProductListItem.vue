<template>
  <div @click="openModal" class="product-card">
    <p class="mypt-title">{{ product.fin_prdt_nm }}</p>
    <p class="mypt-type" :class="{ deposit: isDeposit }">
      {{ product.product_type }}
    </p>
    <div class="mypt-bank">
      <img :src="imgPath" alt="은행 이미지" class="product-img" />
      <p class="bankname">{{ product.kor_co_nm }}</p>
    </div>
    <p class="mypt-date">찜 날짜 | {{ formatDate(product.created_at) }}</p>
  </div>
  <MyProductGraph
    :productDetail="productDetail"
    :isVisible="isVisible"
    :closeModal="closeModal"
  />
</template>

<script setup>
import MyProductGraph from "@/components/Profile/MyProductGraph.vue";
import { useBankStore } from "@/stores/bank";
import axios from "axios";
import { onMounted, ref, watch } from "vue";

const props = defineProps({
  product: Object,
});

const BASE_URL = import.meta.env.VITE_BASE_URL;
const finPrdtCd = props.product.fin_prdt_cd;
const productDetail = ref({});
const isVisible = ref(false);
const isDeposit = ref(false);
const bankStore = useBankStore();
const bankName = props.product.kor_co_nm;
const imgPath = bankStore.bankImage[bankName];

watch(
  () => props.product.product_type,
  (newType) => {
    isDeposit.value = newType === "정기 예금";
  }
);
isDeposit.value = props.product.product_type === "정기 예금";
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
  return props.product.product_type === "정기 적금"
    ? `${BASE_URL}/products/installment_savings/${finPrdtCd}/`
    : `${BASE_URL}/products/deposit/${finPrdtCd}/`;
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

<style scoped>
.product-card {
  cursor: pointer;
}

.product-card:hover {
  box-shadow: 0 0 10px var(--color-primary-blue);
}

.mypt-title {
  font-size: var(--font-size-mlarge);
  font-weight: var(--font-weight-medium);
}

.mypt-type {
  background-color: var(--color-primary-blue);
  color: var(--color-white);
  font-weight: var(--font-weight-medium);
  padding: 0.3rem 0.6rem;
  border-radius: 20px;
  font-size: var(--font-size-small);
}

.deposit {
  background-color: var(--color-primary-beige);
  color: var(--color-black);
}

.mypt-bank {
  display: flex;
  margin: 0 auto;
  align-items: center;
  justify-content: center;
}

.product-img {
  width: 3.5rem;
  margin-right: 0.5rem;
  margin-left: -3rem;
  border-radius: 50%;
}

.bankname {
  font-weight: var(--font-weight-medium);
}
</style>

<template>
  <Carousel v-bind="config">
    <Slide v-for="(product, index) in products" :key="index">
      <div class="carousel__item">
        <RouterLink
          :to="{
            name: 'product_detail',
            params: { product_id: product.fin_prdt_cd },
            query: { product_type: getProductType(product.fin_prdt_nm) },
          }"
        >
          <div class="product-card">
            <div class="product-card-title">
              <img :src="getImagePath(product.kor_co_nm)" alt="은행 이미지" class="bank-img" />
              <p class="product-bank">{{ product.kor_co_nm }}</p>
            </div>
            <p class="product-name">{{ product.fin_prdt_nm }}</p>
          </div>
        </RouterLink>
      </div>
    </Slide>
    <template #addons>
      <Navigation />
    </template>
  </Carousel>
  <Loading :isLoading="isLoading" />
</template>

<script setup>
import "vue3-carousel/dist/carousel.css";
import { Carousel, Slide, Navigation } from "vue3-carousel";
import Loading from "@/components/Common/Loading.vue";
import { onMounted, ref } from "vue";
import axios from "axios";
import { RouterLink, useRoute } from "vue-router";
import { useBankStore } from "@/stores/bank";

const config = {
  autoplay: 2000,
  itemsToShow: 3.95,
  wrapAround: true,
  transition: 500,
  pauseAutoplayOnHover: true,
};

const route = useRoute();
const BASE_URL = import.meta.env.VITE_BASE_URL;
const isLoading = ref(false);
const products = ref([]);
const bankStore = useBankStore();

// 이미지 경로를 가져오는 함수
const getImagePath = (bankName) => {
  return bankStore.bankImage[bankName] || ""; // 해당 은행 이름에 맞는 이미지를 반환
};

// productType 결정 함수
const getProductType = (fin_prdt_nm) => {
  if (fin_prdt_nm.includes("예금")) {
    return "deposits";
  } else if (fin_prdt_nm.includes("적금")) {
    return "savings";
  }
  return ""; // 기본값을 반환하거나 필요에 따라 다른 처리를 할 수 있음
};

const fetchData = async () => {
  isLoading.value = true;
  try {
    const response = await axios({
      method: "get",
      url: `${BASE_URL}/products/random_recommend_list/`,
    });

    // 기존의 products 배열을 초기화
    products.value = []; // 기존 배열 초기화

    // random_deposit에서 각 상품을 개별적으로 추가
    response.data.random_deposit.forEach((deposit) => {
      products.value.push(deposit);
    });

    // random_installment_savings에서 각 상품을 개별적으로 추가
    response.data.random_installment_savings.forEach((savings) => {
      products.value.push(savings);
    });
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false; // 로딩 상태 종료
  }
};

onMounted(async () => {
  await fetchData();
});
</script>

<style>
/* custom style */
.bank-img {
  width: 4rem;
  border-radius: 50%;
}
/* carousel style */
.carousel__slide {
  padding: 5;
}

.carousel__viewport {
  perspective: 2000px;
}

.carousel__track {
  transform-style: preserve-3d;
}

.carousel__slide--sliding {
  transition: 0.5s;
}

.carousel__slide {
  opacity: 0.9;
  transform: rotateY(-20deg) scale(0.9);
}

.carousel__slide--active ~ .carousel__slide {
  transform: rotateY(20deg) scale(0.9);
}

.carousel__slide--prev {
  opacity: 1;
  transform: rotateY(-10deg) scale(0.95);
}

.carousel__slide.carousel__slide--next {
  opacity: 1;
  transform: rotateY(10deg) scale(0.95);
}

.carousel__slide--active {
  opacity: 1;
  transform: rotateY(0) scale(1);
}
</style>

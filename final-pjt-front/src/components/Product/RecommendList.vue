<template>
  <div>
    <h1>상품 추천 목록</h1>
    <!-- <RouterLink :to="{ name: 'product_detail', params: { product_id: product.fin_prdt_cd } }"> -->
    <RecommendListItem v-for="product in recommendProducts" :key="product.fin_prdt_nm" :product="product" />
    <!-- </RouterLink> -->
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import axios from "axios";
import RecommendListItem from "@/components/Product/RecommendListItem.vue";

const userStore = useUserStore();
const router = useRouter();
const recommendProducts = ref([]);

const fetchRecommend = async () => {
  try {
    const response = await axios({
      method: "get",
      url: `${import.meta.env.VITE_BASE_URL}/products/recommend_list/`,
      headers: {
        Authorization: `Token ${userStore.token}`,
      },
    });

    console.log(response.data);
    recommendProducts.value = response.data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  // 1. 로그인하지 않은 사용자의 접근을 막기
  if (!userStore.isLoggedIn) {
    alert("로그인이 필요한 서비스입니다.");
    router.push({ name: "login" });
    return;
  }

  userStore.getUserInfo();
  // 2. 유저의 age, assets, income 정보 확인
  const { age, assets, income } = userStore;

  if (age === null || assets === null || income === null) {
    const confirmed = window.confirm("성별, 나이, 연봉, 자산 정보가 필요해요! 정보 수정 페이지로 이동하시겠어요?");

    if (confirmed) {
      router.push({ name: "my_profile" }); // 정보 수정 페이지로 이동
    } else {
      router.push({ name: "product_deposits" }); // 상품 목록 페이지로 이동
    }
  }

  // 3. 상품 추천 데이터 fetch
  fetchRecommend();
});
</script>

<style scoped></style>

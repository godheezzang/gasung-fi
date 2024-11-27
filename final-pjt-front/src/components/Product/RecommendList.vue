<template>
  <Loading :isLoading="isLoading" />
  <div>
    <div class="product-container">
      <div v-if="recommendProducts.length === 0" class="empty-product">
        <p>추천 상품이 없습니다.</p>
        <p>상품을 둘러보고 찜해보세요.</p>
      </div>
      <div v-else class="product-box">
        <RecommendListItem
          v-for="product in recommendProducts"
          :key="product.fin_prdt_nm"
          :product="product"
        />
      </div>
    </div>

    <Teleport to="body">
      <Modal :show="showModal" @close="showModal = false">
        <template #header>
          <h3>정보 필요</h3>
        </template>
        <template #body>
          <p>
            성별, 나이, 연봉, 자산 정보가 필요해요! 정보 수정 페이지로
            이동하시겠어요?
          </p>
        </template>
        <template #footer>
          <button @click="moveToProfile">네</button>
          <button @click="moveToBack">아니요</button>
        </template>
      </Modal>
    </Teleport>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import axios from "axios";
import RecommendListItem from "@/components/Product/RecommendListItem.vue";
import Modal from "@/components/Common/Modal.vue";
import Loading from "@/components/Common/Loading.vue";

const userStore = useUserStore();
const router = useRouter();
const recommendProducts = ref([]);
const showModal = ref(false);
const isLoading = ref(true);

const fetchRecommend = async () => {
  try {
    const response = await axios({
      method: "get",
      url: `${import.meta.env.VITE_BASE_URL}/products/recommend_list/`,
      headers: {
        Authorization: `Token ${userStore.token}`,
      },
    });
    console.log(response);
    // console.log(response.data);
    recommendProducts.value = response.data;
    isLoading.value = false;
  } catch (error) {
    console.error(error);
    alert("에러가 발생하였습니다.");
    router.go(-1);
  }
};

const moveToProfile = () => {
  showModal.value = false;
  router.push({ name: "my_profile" });
};

const moveToLogin = () => {
  showModal.value = false;
  router.push({ name: "login" });
};

const moveToBack = () => {
  showModal.value = false;
  router.go(-1);
};

onMounted(async () => {
  await userStore.getUserInfo();
  // 2. 유저의 age, assets, income 정보 확인
  const { age, assets, income } = userStore;
  console.log(assets);
  console.log(age);
  console.log(income);
  if (age === null || assets === null || income === null) {
    showModal.value = true;
  } else {
    await fetchRecommend();
  }

  // 3. 상품 추천 데이터 fetch
});
</script>

<style scoped>
.empty-product {
  margin: 2rem auto;
  text-align: center;
}
</style>

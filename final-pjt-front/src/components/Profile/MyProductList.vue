<template>
  <div>
    <h1>내 상품 확인</h1>
    <div v-if="userProducts.length > 0">
      <MyProductListItem v-for="product in userProducts" :key="product.user_product_id" :product="product" />
      <!-- {{ userProducts }} -->
    </div>
    <div v-else>
      <p>현재 찜한 상품이 없어요!</p>
      <p>상품 페이지에서 상품을 둘러보고 상품을 찜해보세요.</p>
      <Button content="상품 둘러보기" ariaLabel="상품목록으로 이동" :onClick="moveToProducts" />
    </div>
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import MyProductListItem from "@/components/Profile/MyProductListItem.vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

const store = useUserStore();
const userProducts = store.userProducts;
const router = useRouter();

const moveToProducts = () => {
  router.push({ name: "products" });
};
</script>

<style scoped></style>

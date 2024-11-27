<template>
  <div>
    <div v-if="userProducts.length > 0" class="product-box">
      <MyProductListItem
        v-for="product in userProducts"
        :key="product.user_product_id"
        :product="product"
      />
      <!-- {{ userProducts }} -->
    </div>
    <div v-else class="product-box">
      <div class="product-wrap">
        <div class="product-none">
          <p>현재 찜한 상품이 없어요!</p>
          <p>상품 페이지에서 상품을 둘러보고 상품을 찜해보세요.</p>
        </div>

        <Button
          content="상품 둘러보기"
          ariaLabel="상품목록으로 이동"
          :onClick="moveToProducts"
        />
      </div>
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

<style scoped>
.product-box {
  margin: 3rem 0;
  /* box-shadow: inset 0 0 20px red; */
}

.product-wrap {
  /* box-shadow: inset 0 0 20px blue; */
  width: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.product-none {
  width: 100%;
  text-align: center;
  margin-bottom: 2rem;
}
</style>

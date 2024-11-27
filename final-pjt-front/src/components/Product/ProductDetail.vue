<template>
  <div class="detail-wrap">
    <Button
      :content="alreadyJoined ? '찜 완료' : '찜하기'"
      :onClick="alreadyJoined ? null : handleJoin"
      ariaLabel="찜하기"
      :customClass="alreadyJoined ? 'disabled-btn' : ''"
      class="bookmark-btn"
    />
    <div v-if="product" class="detail-container">
      <div class="detail-header">
        <div class="detail-header-info">
          <div class="detail-header-title">
            <img :src="imgPath" alt="은행 이미지" class="product-img" />
            <p class="product-title">{{ product.fin_prdt_nm }}</p>
          </div>

          <div class="product-bank-wrap">
            <p class="product-bankname">{{ product.kor_co_nm }}</p>
          </div>
        </div>

        <div class="detail-month">
          <!-- 공시년월일 -->
          <p>{{ product.dcls_month }}</p>
        </div>
      </div>

      <div class="product-desc">
        <div class="product-desc-info">
          <p class="product-desc-title">만기 후 이자율</p>
          <p class="product-desc-info">{{ product.mtrt_int }}</p>
        </div>
        <div class="product-desc-info">
          <p class="product-desc-title">우대 조건</p>
          <p class="product-desc-info">{{ product.spcl_cnd }}</p>
        </div>
        <div class="product-desc-info">
          <p class="product-desc-title">가입 대상</p>
          <p class="product-desc-info">{{ product.join_member }}</p>
        </div>
        <div class="product-desc-info">
          <p class="product-desc-title">가입 제한</p>
          <p class="product-desc-info">{{ product.join_deny_desc }}</p>
        </div>
        <div class="product-desc-info">
          <p class="product-desc-title">가입 방법</p>
          <p class="product-desc-info">{{ product.join_way }}</p>
        </div>
        <div class="product-desc-info">
          <p class="product-desc-title">세부 상품</p>
          <div class="product-options product-desc-info">
            <ul class="product-box">
              <li
                v-for="option in product.options"
                :key="option.id"
                class="product-card"
              >
                <p
                  class="intr-type"
                  :class="{ bokli: option.intr_rate_type_nm === '복리' }"
                >
                  {{ option.intr_rate_type_nm }}
                </p>
                <p>저축 기간: {{ option.save_trm }}개월</p>
                <p>저축 금리: {{ option.intr_rate }}%</p>
                <p>최고 우대금리: {{ option.intr_rate2 }}%</p>
                <Button
                  v-if="store.isStaff"
                  content="금리 수정"
                  :onClick="() => moveToUpdateRate(option.id)"
                  ariaLabel="금리 수정"
                />
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Loading :isLoading="isLoading" />
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import Loading from "@/components/Common/Loading.vue";
import { useBankStore } from "@/stores/bank";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const store = useUserStore();
const router = useRouter();

const isLoading = ref(false);

const finPrdtCd = route.params.product_id;
const productType = route.query.product_type;
const product = ref({});
const alreadyJoined = ref(false);
const bankStore = useBankStore();
const bankName = ref("");
const imgPath = ref("");

// const imgPath = bankStore.bankImage[bankName];

const BASE_URL = import.meta.env.VITE_BASE_URL;

// console.log(productType);
const moveToUpdateRate = (optionId) => {
  console.log(optionId);

  router.push({
    name: "product_edit",
    params: { product_id: finPrdtCd, option_id: optionId },
    query: {
      product_type: productType,
    },
  });
};

// 이미 가입한 상품 목록에서 해당 상품이 있는지 확인
const checkAlreadyJoined = () => {
  alreadyJoined.value = store.userProducts.some(
    (userProduct) => userProduct.fin_prdt_cd === finPrdtCd
  );
  return alreadyJoined.value;
};

alreadyJoined.value = checkAlreadyJoined();

const handleJoin = async () => {
  if (!store.isLoggedIn) {
    const confirmed = window.confirm(
      "로그인된 사용자만 이용할 수 있어요!\n 로그인 화면으로 이동하시겠어요?"
    );

    if (confirmed) {
      router.push({ name: "login" });
    }
    return;
  }

  if (alreadyJoined.value) {
    return;
  }

  const url = getUrl();
  // console.log(url);

  const confirmed = window.confirm("상품을 찜하시겠습니까?");
  if (confirmed) {
    isLoading.value = true;
    try {
      const response = await axios({
        method: "post",
        url,
        headers: {
          Authorization: `Token ${store.token}`,
        },
      });

      // console.log(response.data);
      // 상품 가입 후 사용자 상품 목록 요청
      await store.getUserProducts();
      alreadyJoined.value = true;
      isLoading.value = false;

      alert("상품 찜하기가 완료되었습니다.");
    } catch (error) {
      isLoading.value = false;
      console.error(error);
      alert("상품 찜하기 실패했어요!");
    }
  }
};

// 가입 제한 설명 변환 로직
const changeJoinDenyDesc = (joinDeny) => {
  const descriptions = {
    1: "제한 없음",
    2: "서민 대상",
    3: "일부 제한",
  };
  return descriptions[joinDeny] || "정보 없음";
};

// TODO: Refactor - 상품 상세 정보 불러오는 함수를 productStore에 옮기기
// 이유: 내 상품 확인에서도 사용함. 리팩토링 할 때 이동할 것

// productType에 따라 요청 url 선택하는 로직
const getUrl = () => {
  return productType === "savings"
    ? `${BASE_URL}/products/installment_savings/${finPrdtCd}/`
    : `${BASE_URL}/products/deposit/${finPrdtCd}/`;
};

// 상품 상세 정보 불러오는 로직
// 마운트 될 때 요청
const fetchProductDetail = async () => {
  isLoading.value = true;
  const url = getUrl();
  try {
    const response = await axios({
      method: "get",
      url,
    });

    // console.log(response.data);
    product.value = {
      ...response.data,
      join_deny_desc: changeJoinDenyDesc(Number(response.data.join_deny)),
    };
    bankName.value = product.value.kor_co_nm;
    imgPath.value = bankStore.bankImage[bankName.value];
    isLoading.value = false;
  } catch (error) {
    isLoading.value = false;
    console.error(error);
  }
};
onMounted(async () => {
  isLoading.value = true;
  await fetchProductDetail();
  isLoading.value = false;
});

watch(
  () => store.isStaff,
  (newValue) => {
    console.log(newValue);
    console.log(store.isStaff);
  }
);
</script>

<style scoped>
.detail-wrap {
  width: 50%;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
  min-height: 80vh;
  border: 1px solid var(--color-gray-02);
  /* border-top: unset; */
  /* border-bottom: unset; */
  border-radius: 5px;
  padding: 2rem 2rem 2rem 2rem;
  gap: 1rem;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding-bottom: 1.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--color-gray-02);
}

.detail-header-title {
  display: flex;
  align-items: baseline;
}

.detail-header-info {
  display: flex;
  gap: 2rem;
  align-items: baseline;
}

.detail-month {
  color: var(--color-gray-05);
}

.detail-container {
  padding: 1rem;
}

.bookmark-btn {
  width: fit-content;
  margin-left: auto;
}

.product-title {
  font-size: var(--font-size-extra-large);
  font-weight: var(--font-weight-medium);
}

.product-desc {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.product-desc-title {
  font-size: var(--font-size-large);
  font-weight: var(--font-weight-medium);
  padding: 0.8rem 0;
  border-bottom: 1px solid var(--color-secondary-blue);
  margin-bottom: 1rem;
}

.product-bankname {
  font-size: var(--font-size-small);
  /* margin-top: 1.9rem; */
  color: var(--color-gray-05);
}

.product-img {
  width: 4rem;
  margin-right: 1.5rem;
  display: block;
  margin-bottom: auto;
}

.product-options {
  margin-top: 2rem;
}

.product-card:hover {
  box-shadow: 0 0 5px var(--color-gray-02);
}

.intr-type {
  background-color: var(--color-primary-blue);
  color: var(--color-white);
  border-radius: 40px;
  padding: 0.4rem 0.6rem;
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-small);
}

.intr-type.bokli {
  background-color: var(--color-primary-beige);
  color: var(--color-gray-05);
}
</style>

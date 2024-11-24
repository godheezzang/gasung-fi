<template>
  <div>
    <h1>상품 상세 페이지</h1>
    <Button :content="alreadyJoined ? '찜 완료' : '찜하기'" :onClick="alreadyJoined ? null : handleJoin" ariaLabel="찜하기" :customClass="alreadyJoined ? 'disabled-btn' : ''" />

    <div v-if="product">
      <p>공시 제출월: {{ product.dcls_month }}</p>
      <p>금융 회사명: {{ product.kor_co_nm }}</p>
      <p>상품명: {{ product.fin_prdt_nm }}</p>
      <p>가입 제한: {{ product.join_deny }}</p>
      <p>가입 방법: {{ product.join_way }}</p>
      <p>가입 대상: {{ product.join_member }}</p>
      <p>만기 후 이자율: {{ product.mtrt_int }}</p>
      <p>우대 조건: {{ product.spcl_cnd }}</p>
      <div class="product-options">
        <li v-for="option in product.options" :key="option.deposit_option_id ? option.deposit_option_id : option.installment_savings_option_id">
          <!-- {{ option }} -->
          <p>저축 금리 유형: {{ option.intr_rate_type }}</p>
          <p>저축 금리 유형명: {{ option.intr_rate_type_nm }}</p>
          <p>저축 기간: {{ option.save_trm }}</p>
          <p>저축 금리: {{ option.intr_rate }}</p>
          <p>최고 우대금리: {{ option.intr_rate2 }}</p>
          <Button
            v-if="store.isStaff"
            content="금리 수정"
            :onClick="() => moveToUpdateRate(option.deposit_option_id ? option.deposit_option_id : option.installment_savings_option_id)"
            ariaLabel="금리 수정"
          />
          <hr />
        </li>
      </div>
    </div>
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const store = useUserStore();
const router = useRouter();

const finPrdtCd = route.params.product_id;
const productType = route.query.product_type;
const product = ref({});
const alreadyJoined = ref(false);

const BASE_URL = import.meta.env.VITE_BASE_URL;

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
  alreadyJoined.value = store.userProducts.some((userProduct) => userProduct.fin_prdt_cd === finPrdtCd);
  return alreadyJoined.value;
};

alreadyJoined.value = checkAlreadyJoined();

const handleJoin = async () => {
  if (!store.isLoggedIn) {
    const confirmed = window.confirm("로그인된 사용자만 이용할 수 있어요!\n 로그인 화면으로 이동하시겠어요?");

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
      alert("상품 가입이 완료되었습니다.");
    } catch (error) {
      console.error(error);
      alert("상품 가입에 실패했어요!");
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

// TODO: 상품 상세 정보 불러오는 함수를 productStore에 옮기기
// 이유: 내 상품 확인에서도 사용함. 리팩토링 할 때 이동할 것

// productType에 따라 요청 url 선택하는 로직
const getUrl = () => {
  return productType === "saving" ? `${BASE_URL}/products/installment_savings/${finPrdtCd}/` : `${BASE_URL}/products/deposit/${finPrdtCd}/`;
};

// 상품 상세 정보 불러오는 로직
// 마운트 될 때 요청
const fetchProductDetail = async () => {
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
  } catch (error) {
    console.error(error);
  }
};
onMounted(() => {
  fetchProductDetail();
});

watch(
  () => store.isStaff,
  (newValue) => {
    console.log(newValue);
    console.log(store.isStaff);
  }
);
</script>

<style scoped></style>

<template>
  <div class="update-wrap">
    <div class="update-container">
      <div class="update-header">
        <img :src="imgPath" alt="은행 이미지" class="product-img" />
        <p class="product-title">{{ fin_prdt_nm }}</p>
      </div>
      <form @submit.prevent="updateRate" class="update-form-wrap">
        <div class="update-form">
          <label for="intr_rate" class="update-label">저축 금리</label>
          <input type="number" id="intr_rate" v-model="intrRate" step="0.01" class="user-input" placeholder="숫자만 입력해주세요." />
        </div>

        <div class="update-form">
          <label for="intr_rate2" class="update-label">최고 우대금리</label>
          <input type="number" id="intr_rate2" v-model="intrRate2" step="0.01" class="user-input" placeholder="숫자만 입력해주세요." />
        </div>
        <Button content="수정 완료" ariaLabel="수정 완료" type="submit" class="update-btn"></Button>
      </form>
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
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const userStore = useUserStore();
const router = useRouter();
const route = useRoute();

const BASE_URL = import.meta.env.VITE_BASE_URL;
const finPrdtCd = route.params.product_id;
const productType = route.query.product_type;

const optionId = route.params.option_id;
const intrRate = ref("");
const intrRate2 = ref("");
const options = ref([]);
const option = ref({});
const isLoading = ref(false);
const bankStore = useBankStore();
const bankName = ref("");
const imgPath = ref("");
const fin_prdt_nm = ref("");

const getUrl = () => {
  return productType === "saving" ? `${BASE_URL}/products/installment_savings/${finPrdtCd}/` : `${BASE_URL}/products/deposit/${finPrdtCd}/`;
};

const getUpdateUrl = (productType) => {
  console.log(productType);

  if (productType === "deposits") {
    return `${BASE_URL}/products/deposit/${finPrdtCd}/${optionId}/`;
  } else if (productType === "savings") {
    return `${BASE_URL}/products/installment_savings/${finPrdtCd}/${optionId}/`;
  }
};

const updateRate = async () => {
  isLoading.value = true;
  const url = getUpdateUrl(productType);
  console.log(url);

  try {
    const response = await axios({
      method: "put",
      url,
      data: {
        intr_rate: intrRate.value,
        intr_rate2: intrRate2.value,
      },
      headers: {
        Authorization: `Token ${userStore.token}`,
      },
    });
    console.log(response);
    if (response.status === 200) {
      isLoading.value = false;
      alert("수정이 완료되었습니다.");
      router.push({
        name: "product_detail",
        params: { product_id: finPrdtCd },
      });
    }
  } catch (error) {
    isLoading.value = false;
    console.error(error);
    alert("요청에 실패하였습니다.");
  }
};

const fetchData = async () => {
  isLoading.value = true;
  const url = getUrl();
  try {
    const response = await axios({
      method: "get",
      url,
    });

    // console.log(response);
    options.value = response.data.options;
    // console.log(options.value);

    option.value = options.value.find((option) => option.id);
    // console.log(option.value);
    fin_prdt_nm.value = response.data.fin_prdt_nm;
    intrRate.value = option.value.intr_rate;
    intrRate2.value = option.value.intr_rate2;
    bankName.value = response.data.kor_co_nm;
    imgPath.value = bankStore.bankImage[bankName.value];
    isLoading.value = false;
  } catch (error) {
    isLoading.value = false;
    console.error(error);
  }
};
onMounted(async () => {
  isLoading.value = true;
  if (!userStore.isStaff) {
    isLoading.value = false;
    alert("관리자만 접근이 가능합니다.");
    router.go(-1);
  }

  await fetchData();
  isLoading.value = false;
});
</script>

<style scoped>
.update-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;

  flex-direction: column;
}

.update-header p {
  font-size: var(--font-size-large);
  font-weight: var(--font-weight-bold);
}
.product-img {
  width: 3rem;
}
.update-wrap {
  /* box-shadow: inset 0 0 20px red; */
  width: 70%;
  margin: 0 auto;
}

.update-container {
  /* box-shadow: inset 0 0 20px blue; */
  margin: 0 auto;
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 50%;
  border: 1px solid var(--color-gray-02);
  border-radius: 5px;
  gap: 2rem;
  padding: 2rem;
}

.update-form-wrap {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  gap: 2rem;
}

.user-input {
  border-radius: 5px;
  height: 4rem;
  width: 50%;
  text-align: center;
}

.update-form {
  /* box-shadow: inset 0 0 20px purple; */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.update-label {
  font-size: var(--font-size-mlarge);
  font-weight: var(--font-weight-medium);
}

.update-btn {
  width: 60%;
  margin: 0 auto;
}
</style>

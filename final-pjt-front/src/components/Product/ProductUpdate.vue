<template>
  <div>
    <h1>금리 수정</h1>
    <form @submit.prevent="updateRate">
      <label for="intr_rate">저축 금리: </label>
      <input type="number" id="intr_rate" v-model="intrRate" step="0.01" />
      <br />
      <label for="intr_rate2">최고 우대금리: </label>
      <input type="number" id="intr_rate2" v-model="intrRate2" step="0.01" />
      <Button content="수정 완료" ariaLabel="수정 완료" type="submit"></Button>
    </form>
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
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
console.log(productType);

const optionId = route.params.option_id;
const intrRate = ref("");
const intrRate2 = ref("");
const options = ref([]);
const option = ref({});

const getUrl = () => {
  return productType === "saving" ? `${BASE_URL}/products/installment_savings/${finPrdtCd}/` : `${BASE_URL}/products/deposit/${finPrdtCd}/`;
};

const getUpdateUrl = (productType) => {
  console.log(productType);

  if (productType === "deposit") {
    return `${BASE_URL}/products/deposit/${finPrdtCd}/${optionId}/`;
  } else if (productType === "saving") {
    return `${BASE_URL}/products/installment_savings/${finPrdtCd}/${optionId}/`;
  }
};

const updateRate = async () => {
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
    // console.log(response);
    if (response.status === 200) {
      alert("수정이 완료되었습니다.");
      router.push({ name: "product_detail", params: { product_id: finPrdtCd } });
    }
  } catch (error) {
    console.error(error);
  }
};

const fetchData = async () => {
  const url = getUrl();
  try {
    const response = await axios({
      method: "get",
      url,
    });

    // console.log(response);
    options.value = response.data.options;
    // console.log(options.value);

    option.value = options.value.find((option) => (option.deposit_option_id ? option.deposit_option_id : option.installment_savings_option_id));
    // console.log(option.value);
    intrRate.value = option.value.intr_rate;
    intrRate2.value = option.value.intr_rate2;
  } catch (error) {
    console.error(error);
  }
};
onMounted(() => {
  if (!userStore.isStaff) {
    alert("관리자만 접근이 가능합니다.");
    router.go(-1);
  }

  fetchData();
});
</script>

<style scoped></style>

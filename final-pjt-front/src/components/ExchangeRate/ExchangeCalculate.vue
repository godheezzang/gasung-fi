<template>
  <div>
    <div>
      <label for="country">국가 선택:</label>
      <select id="country" v-model="selectedCountry">
        <option value="" disabled>선택하세요</option>
        <option v-for="country in countries" :key="country.cur_unit" :value="country">{{ country.country }}</option>
      </select>
      <input type="number" />
    </div>

    <div>
      <label for="koreanMoney">한국 원화:</label>
      <input type="text" id="koreanMoney" v-model.number="kMoneyInput" @input="convertMoney" /> 원
    </div>

    <div v-if="convertedAmount !== null">
      <p>변환된 금액: {{ convertedAmount }} {{ selectedCountry?.money }}</p>
    </div>
    <div v-else>
      <p>환율 정보를 선택하세요.</p>
    </div>
  </div>
</template>
<!-- TODO: 환율계산 완성하기 -->
<script setup>
import { useRateStore } from "@/stores/exchangeRate";
import { onMounted, ref, computed, watch } from "vue";

const store = useRateStore();
const selectedCountry = ref(null);
const convertedAmount = ref(1);
const kMoneyInput = ref("");

// 국가 리스트를 formattedRates에서 추출
const countries = computed(() => {
  return store.formattedRates.map((rate) => ({
    country: rate.country,
    cur_unit: rate.cur_unit,
    bkpr: rate.bkpr,
    money: rate.money, // 통화 이름
  }));
});

console.log(selectedCountry.value);

// const kMoneyInput = ref(selectedCountry.value.bkpr);

// 환율 변환 함수
const convertMoney = () => {
  if (selectedCountry.value && !isNaN(kMoneyInput.value)) {
    const bkprStr = selectedCountry.value.bkpr; // 선택된 국가의 bkpr
    const bkpr = Number(bkprStr.replace(/,/g, "")); // 쉼표 제거 및 숫자로 변환

    if (!isNaN(bkpr)) {
      convertedAmount.value = (kMoneyInput.value / bkpr).toFixed(2); // 변환된 금액 계산
    } else {
      convertedAmount.value = null; // bkpr가 유효하지 않은 경우
    }
  } else {
    convertedAmount.value = null; // 국가가 선택되지 않았거나 입력이 유효하지 않은 경우
  }
};

// 선택된 국가가 변경될 때마다 변환 계산
watch(selectedCountry, convertMoney);

const fetchRate = async () => {
  await store.getRate();
};

onMounted(() => {
  fetchRate();
});
</script>

<style scoped>
/* 스타일을 추가할 수 있습니다 */
</style>

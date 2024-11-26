<template>
  <div>
    <div>
      <label for="country">국가 선택:</label>
      <select class="custom-select" id="country" v-model="selectedCountry">
        <option value="" disabled>선택하세요</option>
        <option
          v-for="country in countries"
          :key="country.cur_unit"
          :value="country"
        >
          {{ country.country }}
        </option>
      </select>
    </div>

    <div>
      <label for="koreanMoney">한국 원화 : </label>
      <input
        type="number"
        id="koreanMoney"
        v-model.number="kMoneyInput"
        @input="convertToForeign"
      />
      <span>원</span>
    </div>

    <div v-if="convertedAmount !== null">
      <label for="foreignMoney"
        >{{ selectedCountry.country }} {{ selectedCountry.money }} :
      </label>
      <input
        type="number"
        id="foreignMoney"
        v-model.number="foreignMoneyInput"
        @input="convertToKorean"
      />
      <span>{{ selectedCountry.money }}</span>
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
const convertedAmount = ref(null);
const kMoneyInput = ref("");
const foreignMoneyInput = ref("");

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
const convertToForeign = () => {
  if (selectedCountry.value && !isNaN(kMoneyInput.value)) {
    const bkprStr = selectedCountry.value.bkpr; // 선택된 국가의 bkpr
    const bkpr = Number(bkprStr.replace(/,/g, "")); // 쉼표 제거 및 숫자로 변환

    if (!isNaN(bkpr)) {
      convertedAmount.value = (kMoneyInput.value / bkpr).toFixed(2); // 변환된 금액 계산
      foreignMoneyInput.value = convertedAmount.value; // 외국 통화 입력 필드 업데이트
    } else {
      convertedAmount.value = null; // bkpr가 유효하지 않은 경우
    }
  } else {
    convertedAmount.value = null; // 국가가 선택되지 않았거나 입력이 유효하지 않은 경우
    foreignMoneyInput.value = 0; // 외국 통화 입력 필드 초기화
  }
};
const convertToKorean = () => {
  if (selectedCountry.value && !isNaN(foreignMoneyInput.value)) {
    const bkprStr = selectedCountry.value.bkpr; // 선택된 국가의 bkpr
    const bkpr = Number(bkprStr.replace(/,/g, "")); // 쉼표 제거 및 숫자로 변환

    if (!isNaN(bkpr)) {
      kMoneyInput.value = (foreignMoneyInput.value * bkpr).toFixed(2); // 변환된 금액 계산
    } else {
      kMoneyInput.value = 0; // bkpr가 유효하지 않은 경우
    }
  } else {
    kMoneyInput.value = 0; // 국가가 선택되지 않았거나 입력이 유효하지 않은 경우
  }
};
// const convertMoney = () => {
//   if (selectedCountry.value && !isNaN(kMoneyInput.value)) {
//     const bkprStr = selectedCountry.value.bkpr; // 선택된 국가의 bkpr
//     const bkpr = Number(bkprStr.replace(/,/g, "")); // 쉼표 제거 및 숫자로 변환
//
//     if (!isNaN(bkpr)) {
//       convertedAmount.value = (kMoneyInput.value / bkpr).toFixed(2); // 변환된 금액 계산
//     } else {
//       convertedAmount.value = null; // bkpr가 유효하지 않은 경우
//     }
//   } else {
//     convertedAmount.value = null; // 국가가 선택되지 않았거나 입력이 유효하지 않은 경우
//   }
// };

// 선택된 국가가 변경될 때마다 변환 계산
watch(selectedCountry, () => {
  convertToForeign();
  convertToKorean();
});

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

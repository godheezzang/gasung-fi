<template>
  <div class="cal-container">
    <div class="cal-wrap">
      <div class="cal-inputs">
        <label for="country">국가 선택</label>
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

      <div class="cal-inputs">
        <label for="koreanMoney">한국 원화</label>
        <input
          type="number"
          id="koreanMoney"
          v-model.number="kMoneyInput"
          @input="convertToForeign"
          class="user-input"
          placeholder="0.00"
        />
        <span>원</span>
      </div>

      <div v-if="convertedAmount !== null" class="cal-inputs">
        <label for="foreignMoney"
          >{{ selectedCountry.country }} {{ selectedCountry.money }}</label
        >
        <input
          type="number"
          id="foreignMoney"
          v-model.number="foreignMoneyInput"
          @input="convertToKorean"
          class="user-input"
          placeholder="0.00"
        />
        <span> {{ selectedCountry.money }}</span>
      </div>
      <div v-else>
        <p class="err-msg">국가를 선택하세요.</p>
      </div>
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

// console.log(selectedCountry.value);

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
.cal-container {
  /* box-shadow: inset 0 0 20px red; */
  width: 50%;
  margin: 0 auto;
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.cal-wrap {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cal-inputs {
  width: 100%;
}
.cal-inputs label {
  font-size: var(--font-size-mlarge);
  font-weight: var(--font-weight-medium);
  margin-right: 0.5rem;
}
.cal-inputs span {
  margin-left: 1rem;
}

.user-input {
  border-radius: 5px;
}

.err-msg {
  text-align: center;
  font-size: var(--font-size-medium);
}
</style>

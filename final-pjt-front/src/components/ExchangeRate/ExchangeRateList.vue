<template>
  <div>
    <div v-if="isLoading">Loading...</div>
    <div v-else-if="rateInfos" class="rate-container">
      <ExchangeRateListItem v-for="rate in rateInfos" :key="rate.cur_unit" :rate="rate" class="rate-card" />
    </div>
    <!-- TODO: 환율 정보 불러올 수 없을 경우 에러 페이지 -->
    <div v-else>환율 정보를 불러올 수 없습니다.</div>
  </div>
</template>

<script setup>
import ExchangeRateListItem from "@/components/ExchangeRate/ExchangeRateListItem.vue";
import { useRateStore } from "@/stores/exchangeRate";
import { onMounted, ref, watch } from "vue";

const store = useRateStore();
const rateInfos = ref(null);
const isLoading = ref(true);

const fetchRate = async () => {
  await store.getRate();
  rateInfos.value = store.formattedRates;
  isLoading.value = false;
};

onMounted(() => {
  fetchRate();
});
</script>

<style scoped>
.rate-container {
  box-shadow: inset 0 0 20px blue;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.rate-card {
  /* box-shadow: inset 0 0 20px red; */
  border: 1px solid var(--color-gray-04);
  /* flex-grow: 1; */
  flex-shrink: 0;
  flex-basis: 100%;
  max-width: 30%;
}
</style>

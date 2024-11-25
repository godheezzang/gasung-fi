<template>
  <div>
    <Loading :isLoading="isLoading" />

    <div class="rate-container product-box">
      <ExchangeRateListItem v-for="rate in rateInfos" :key="rate.cur_unit" :rate="rate" class="product-card" />
    </div>
    <!-- TODO: 환율 정보 불러올 수 없을 경우 에러 페이지 -->
  </div>
</template>

<script setup>
import Loading from "@/components/Common/Loading.vue";
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
  /* box-shadow: inset 0 0 20px blue; */
  display: flex;
  flex-wrap: wrap;
  gap: 3rem;
  padding: 3rem 2rem;
}
</style>

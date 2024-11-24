<template>
  <div>
    <RouterLink :to="{ name: 'exchange_rate_home' }">환율 정보</RouterLink>
    <RouterLink :to="{ name: 'exchange-rate_calcuate' }">환율 계산</RouterLink>
  </div>
  <RouterView />
</template>

<script setup>
import ExchangeRateList from "@/components/ExchangeRate/ExchangeRateList.vue";
</script>

<style scoped></style>

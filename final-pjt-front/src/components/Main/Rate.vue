<template>
  <Carousel v-bind="config">
    <Slide v-for="(rate, index) in rateInfos" :key="index">
      <div class="carousel__item">
        <div class="product-card">
          <p class="rate-country">{{ rate.country }}</p>
          <p>사실 때: {{ rate.ttb }}{{ rate.money }}</p>
          <p>파실 때: {{ rate.tts }}{{ rate.money }}</p>
        </div>
      </div>
    </Slide>
    <template #addons>
      <Navigation />
    </template>
  </Carousel>
</template>

<script setup>
import "vue3-carousel/dist/carousel.css";
import { Carousel, Slide, Pagination, Navigation } from "vue3-carousel";
import { useRateStore } from "@/stores/exchangeRate";
import { onMounted, ref } from "vue";

const config = {
  itemsToShow: 2.5,
  wrapAround: true,
  autoplay: 2000,
};

const rateStore = useRateStore();
const rateInfos = ref(null);
const isLoading = ref(false);

const fetchRate = async () => {
  isLoading.value = true;
  await rateStore.getRate();
  rateInfos.value = rateStore.formattedRates;
  isLoading.value = false;
  // console.log(rateInfos.value);
};

onMounted(async () => {
  isLoading.value = true;
  await rateStore.getRate();
  await fetchRate();
  isLoading.value = false;
});
</script>

<style>
.product-card:hover {
  box-shadow: 0 0 5px var(--color-gray-02);
}

.rate-country {
  font-size: var(--font-size-mlarge);
  font-weight: var(--font-weight-medium);
}
</style>

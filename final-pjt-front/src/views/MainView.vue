<template>
  <div class="main-container">
    <div class="main-carousel">
      <h1 class="carousel-title">오늘의 추천 예적금 상품</h1>
      <Carousel />
    </div>
    <div class="main-preview">
      <div class="main-community">
        <p class="preview-title">신규 게시글</p>
        <p class="preview-desc">실시간 최신 게시글을 확인해 보세요.</p>
        <RouterLink :to="{ name: 'community' }">커뮤니티 바로가기</RouterLink>
        <Community />
      </div>
      <div class="main-rate">
        <p class="preview-title">주요 환율 정보</p>
        <p class="preview-desc">주요 환율 정보를 확인해 보세요.</p>
        <p class="preview-desc-add">한국 원화 1원 대비 환율입니다.</p>
        <Rate />
      </div>
    </div>
  </div>
</template>

<script setup>
import Carousel from "@/components/Main/Carousel.vue";
import Community from "@/components/Main/Community.vue";
import Rate from "@/components/Main/Rate.vue";
import { ref } from "vue";
import { RouterLink, RouterView } from "vue-router";
</script>

<style scoped>
.main-container {
  /* box-shadow: inset 0 0 20px red; */
  width: 70%;
  margin: 2rem auto;
  /* min-height: 80rem; */
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.main-carousel {
  /* box-shadow: inset 0 0 20px blue; */
  flex-grow: 1.5;
}

.carousel-title {
  font-size: var(--font-size-extra-large);
  font-weight: var(--font-weight-medium);
  margin-bottom: 2rem;
}

.main-preview {
  /* box-shadow: inset 0 0 20px purple; */
  flex-grow: 1;
  display: flex;
}

.preview-title {
  font-size: var(--font-size-large);
  font-weight: var(--font-weight-medium);
}

.preview-desc {
  margin-top: 0.5rem;
}

.preview-desc-add {
  color: var(--color-gray-04);
  margin-bottom: 2rem;
}
.main-community {
  /* box-shadow: inset 0 0 20px orchid; */
  flex-grow: 1;
}

.main-rate {
  /* box-shadow: inset 0 0 20px salmon; */
  flex-grow: 1;
  max-width: 50%;
}
</style>

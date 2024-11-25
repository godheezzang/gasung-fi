<template>
  <div style="display: flex; align-items: center">
    <span v-if="leftmostPage > PAGE_PER_SECTION">
      <a
        @click="
          () => {
            leftmostPage -= PAGE_PER_SECTION;
            onChangeCurPage(leftmostPage);
          }
        "
        >&lt;</a
      >
    </span>
    <span class="page" v-for="page in getPaginationArray(leftmostPage)" :key="page">
      <a
        :class="{ on: page === curPage }"
        @click="
          () => {
            onChangeCurPage(page);
          }
        "
      >
        {{ page }}</a
      >
    </span>
    <span v-if="leftmostPage + PAGE_PER_SECTION <= totalPage">
      <a
        @click="
          () => {
            leftmostPage += PAGE_PER_SECTION;
            onChangeCurPage(leftmostPage);
          }
        "
        >&gt;</a
      >
    </span>
  </div>
  <p>totalArticles : {{ list.length }}</p>
  <p>totalPage : {{ totalPage }}</p>
  <p>leftmostPage : {{ leftmostPage }}</p>
  <p>ITEM_PER_PAGE : {{ ITEM_PER_PAGE }}</p>
  <p>PAGE_PER_SECTION : {{ PAGE_PER_SECTION }}</p>
</template>

<script setup>
import { computed, ref } from "vue";

const props = defineProps({
  list: Array,
  ITEM_PER_PAGE: Number,
  PAGE_PER_SECTION: Number,
});

const emit = defineEmits(["change-page"]);

const curPage = ref(1);
const leftmostPage = ref(1);
const totalPage = computed(() => Math.ceil(props.list.length / (props.ITEM_PER_PAGE || 1)));

const getPaginationArray = (left) => {
  const res = [];
  for (let i = left; i < Math.min(totalPage.value + 1, left + props.PAGE_PER_SECTION); i++) {
    res.push(i);
  }
  return res;
};

const onChangeCurPage = (page) => {
  curPage.value = page;
  emit("change-page", page);
};
</script>

<style>
.page {
  padding: 1rem;
  cursor: pointer;
}
.page a.on {
  font-weight: 900;
  color: red;
}
</style>

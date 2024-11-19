<template>
  <form class="search-form" @submit.prevent="handleSearch">
    <input
      type="text"
      v-model="searchInput"
      placeholder="검색어를 입력하세요."
      class="search-input"
    />
    <button @click="handleDelete">
      <img src="@/assets/icons/x_btn.svg" alt="검색어 삭제" />
    </button>
    <button type="submit" aria-label="search">
      <img src="@/assets/icons/search.svg" alt="검색" />
    </button>
  </form>
</template>

<script setup>
const props = defineProps({
  searchPath: {
    type: String,
    required: true,
  },
});
import { ref } from "vue";
import { useRouter } from "vue-router";

const searchInput = ref("");
const router = useRouter();
const handleSearch = () => {
  // 검색 버튼 눌렀을 때 향하는 경로
  const pathName = props.searchPath;
  router.push({ name: `${pathName}`, query: { search: searchInput.value } });
};

const handleDelete = () => {
  searchInput.value = "";
};
</script>

<style scoped></style>

<template>
  <div class="article-per">
    <div class="article-wrap">
      <div v-if="articles.length > 0" class="article-container">
        <div class="article-item">
          <div class="article-desc">
            <p class="article-id">글 번호</p>
            <p class="article-title">제목</p>
            <p class="article-username">작성자</p>
          </div>
        </div>
        <ArticleListItem
          v-for="article in articles"
          :key="article.id"
          :article="article"
        />
      </div>
      <Button :onClick="moveToCreate" content="글쓰기" ariaLabel="글쓰기" />
      <div v-if="articles.length === 0" class="blank_list article-container">
        <p>게시글이 없습니다.</p>
      </div>

      <div class="pagination">
        <button
          @click="prevPage"
          :disabled="currentPage === 1"
          class="previous-icon"
        >
          <img src="@/assets/icons/arrow_forward.svg" alt="이전" />
        </button>
        <span>{{ currentPage }} / {{ totalPages }}</span>
        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="next-icon"
        >
          <img src="@/assets/icons/arrow_forward.svg" alt="다음" />
        </button>
      </div>
      <Loading :isLoading="isLoading" />
    </div>
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import Loading from "@/components/Common/Loading.vue";
import ArticleListItem from "@/components/Community/ArticleListItem.vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const articles = ref([]);
const isLoading = ref(true);
const currentPage = ref(1);
const totalPages = ref(0);
const productsPerPage = 10;
const BASE_URL = import.meta.env.VITE_BASE_URL;
const userStore = useUserStore();

const moveToCreate = () => {
  router.push({ name: "create_article" });
};

const getArticles = async (page = 1) => {
  try {
    const response = await axios({
      method: "get",
      url: `${BASE_URL}/articles/`,
      params: {
        page,
      },
    });
    // console.log(response);
    if (response.status === 200 && response.data) {
      articles.value = response?.data.results;
      totalPages.value = Math.ceil(response.data.count / productsPerPage);
      isLoading.value = false;
      // console.log(articles.value);
    }
    // console.log(articles.value);
  } catch (error) {
    console.error(error);
    isLoading.value = false;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;

    getArticles(currentPage.value);
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    getArticles(currentPage.value);
  }
};

onMounted(async () => {
  await getArticles(currentPage.value);
  // console.log(articles.value);
  // console.log(articles.length === 0);
});
</script>

<style scoped>
.article-per {
  width: 70%;
  margin: 0 auto;
}
.article-wrap {
  /* box-shadow: inset 0 0 20px blue; */
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  min-height: 63rem;
}

.article-wrap .default-btn {
  flex-grow: 0;
  width: fit-content;
  margin-left: auto;
  padding: 0.5rem 1rem;
  font-size: var(--font-size-extra-small);
  background-color: var(--color-white);
  color: var(--color-gray-04);
  border-radius: 5px;
  border: 1px solid var(--color-gray-04);
  margin-right: 10rem;
  margin-top: auto;
}

.blank_list {
  width: 100%;
  text-align: center;
}

.blank_list p {
  margin-bottom: 5rem;
}

.article-container {
  /* box-shadow: inset 0 0 20px red; */
  width: 70%;
  margin: 0 auto;
}

.article-item {
  /* box-shadow: inset 0 0 20px green; */
  padding: 2rem;
  border-bottom: 2px solid var(--color-gray-02);
}

.article-desc {
  display: flex;
  gap: 2rem;
  height: 1rem;
  align-items: center;
  text-align: center;
}

.article-id {
  flex-grow: 1;
  flex-grow: 1;
  flex-basis: 6rem;
  text-align: center;
  flex-shrink: 0;
  border-right: 1px solid var(--color-gray-01);
  max-width: 10rem;
}

.article-title {
  flex-grow: 2;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  word-break: break-all;
  max-width: 50rem;
}

.article-username {
  flex-grow: 1;
  text-align: center;
  flex-shrink: 0;
  max-width: 15rem;
}

.pagination {
  margin-top: auto;
}
</style>

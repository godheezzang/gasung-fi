<template>
  <div>
    <ul class="article-container">
      <li v-for="article in articles" :key="article.id">
        <RouterLink :to="{ name: 'article_detail', params: { article_id: article.id } }">
          <div class="article-content">
            <p class="article-title">{{ article.title }}</p>
            <p>{{ article.username }}</p>
          </div>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";

const BASE_URL = import.meta.env.VITE_BASE_URL;
const isLoading = ref(false);
const articles = ref("");

const fetchData = async (page = 1) => {
  isLoading.value = true;
  try {
    const response = await axios({
      method: "get",
      url: `${BASE_URL}/articles/`,
      params: {
        page,
      },
    });

    // console.log(response);
    articles.value = response.data.results.slice(0, 7);
    isLoading.value = false;
    // console.log(articles.value);
  } catch (error) {
    isLoading.value = false;
    console.error(error);
  }
};

onMounted(async () => {
  isLoading.value = true;
  await fetchData();
  isLoading.value = false;
});
</script>

<style scoped>
.article-container {
  /* box-shadow: inset 0 0 20px red; */
  margin: 0 auto;
  margin-top: 1rem;
  max-width: calc(100% - 4rem);
}

.article-content {
  /* box-shadow: inset 0 0 20px lime; */
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
}

.article-content:hover {
  cursor: pointer;
}

.article-content:hover .article-title {
  color: var(--color-primary-blue);
}
</style>

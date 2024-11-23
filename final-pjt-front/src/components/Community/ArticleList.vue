<template>
  <div>
    <h2>게시글 목록</h2>
    <div v-if="articles.length > 0">
      <ArticleListItem v-for="article in articles" :key="article.article_id" :article="article" />
    </div>
    <div v-else>게시글이 없습니다.</div>
  </div>
  <Button :onClick="moveToCreate" content="글쓰기" ariaLabel="글쓰기" />
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import ArticleListItem from "@/components/Community/ArticleListItem.vue";
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const articles = ref([]);

const moveToCreate = () => {
  router.push({ name: "create_article" });
};

const getArticles = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_BASE_URL}/articles/`);
    console.log(response);
    const contentType = response.headers["content-type"];
    if (response.status === 200 && response.data) {
      articles.value = response?.data;
    }
    // console.log(articles.value);
  } catch (error) {
    console.error(error);
  }
};
onMounted(() => {
  getArticles();
  // console.log(articles.value);
  // console.log(articles.length === 0);
});
</script>

<style scoped></style>

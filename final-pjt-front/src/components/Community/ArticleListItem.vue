<template>
  <div>
    <RouterLink
      :to="{
        name: 'article_detail',
        params: { article_id: article.article_id },
      }"
    >
      {{ article.article_id }} | {{ article.title }}
      <span>({{ article.comment_count }})</span>
      <span></span>
    </RouterLink>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";

const props = defineProps({
  article: Object,
});

// console.log(props.article);
</script>

<style scoped></style>

<template>
  <div>
    <h2>게시글 상세</h2>
    <div>
      <p>글 번호: {{ article.article_id }}</p>
      <p>제목: {{ article.title }}</p>
      <p>작성자: {{ article.username }}</p>
      <hr />
      <p>작성일: {{ formattedCreatedAt }}</p>
      <p>수정일: {{ formattedUpdatedAt }}</p>
      <hr />
      <p>내용</p>
      <p>{{ article.content }}</p>
    </div>
    <hr />
    <div>
      <p>
        <span>{{ article.comment_count }}개의 댓글</span>
      </p>
      <CommentListItem v-if="article.comment_count" v-for="comment in article.comments" :key="comment.comment_id" :comment="comment" />
      <div v-if="!article.comment_count">댓글이 없습니다.</div>
    </div>
    <CommentCreate />
    <!-- TODO: 사용자 동일 여부에 따라 삭제, 수정버튼 렌더링 -->
    <Button content="목록" :onClick="moveToList" ariaLabel="게시글 목록" />
    <Button v-if="article.email === store.userEmail" content="삭제" :onClick="handleDelete" ariaLabel="게시글 삭제" />
    <Button v-if="article.email === store.userEmail" content="수정" :onClick="moveToUpdate" ariaLabel="게시글 수정" />
  </div>
</template>

<script setup>
import Button from "@/components/Common/Button.vue";
import CommentCreate from "@/components/Community/CommentCreate.vue";
import CommentListItem from "@/components/Community/CommentListItem.vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const articleId = route.params.article_id;
const article = ref("");
const store = useUserStore();

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, "0");

  const formattedTime = (hours === 0 ? 24 : hours) + ":" + minutes;

  return `${year}년  ${month}월 ${day}일 ${formattedTime}`;
};

const formattedCreatedAt = computed(() => formatDate(article.value.created_at));
const formattedUpdatedAt = computed(() => formatDate(article.value.updated_at));

const moveToList = () => {
  router.push({ name: "community" });
};

const handleDelete = async () => {
  window.confirm("게시글을 삭제하시겠습니까?");
  if (confirm) {
    try {
      const response = await axios.delete(`${import.meta.env.VITE_BASE_URL}/articles/${articleId}/`, {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      });

      // console.log(response);
      if (response.status === 204) {
        router.push({ name: "community" });
      }
    } catch (error) {
      console.error(error);
    }
  }
};

const moveToUpdate = () => {
  router.push({ name: "create_article", query: { article_id: articleId } });
};

const getDetailArticle = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_BASE_URL}/articles/${articleId}/`);

    if (response.status === 200) {
      console.log(response);
      article.value = response.data;
    }
  } catch (error) {
    console.error(error);
  }
};
onMounted(() => {
  getDetailArticle();
});
</script>

<style scoped></style>

<script setup>
import "@/assets/main.css";
import Navbar from "@/components/Header/Navbar.vue";
import Menubar from "@/components/Header/Menubar.vue";

import Modal from "@/components/Common/Modal.vue";
import { ref } from "vue";
import { RouterView, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";

const showModal = ref(false);
const router = useRouter();
const userStore = useUserStore();

const redirectToLogin = () => {
  console.log("log");
  router.push({ name: "login" }); // 로그인 페이지로 이동
  showModal.value = false; // 모달 닫기
};

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    showModal.value = true; // 모달 표시
    return next(false); // 라우팅 중단
  } else {
    next(); // 라우팅 진행
  }

  if ((userStore.isLoggedIn && to.path === "/login") || to.path === "signup") {
    return next({ path: "/" });
  }
});
</script>

<template>
  <div class="container">
    <nav>
      <Navbar />
      <Menubar />
    </nav>
    <main>
      <RouterView />
      <div>
        <Teleport to="body">
          <Modal :show="showModal" @close="showModal = false">
            <template #header>
              <h3>로그인 필요</h3>
            </template>
            <template #body>
              <p>로그인이 필요한 서비스입니다.</p>
              <p>로그인하시고 이용해보세요!</p>
            </template>
            <template #footer>
              <button
                @click="
                  () => {
                    console.log('Redirect button clicked');
                    redirectToLogin();
                  }
                "
              >
                확인
              </button>

              <button @click="showModal = false">취소</button>
            </template>
          </Modal>
        </Teleport>
      </div>
    </main>
  </div>
</template>

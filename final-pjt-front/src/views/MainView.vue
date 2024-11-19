<template>
  <div class="main">
    <h1 class="title">Main</h1>
  </div>
  <RouterView />
</template>

<script setup>
import Search from "@/components/Common/Search.vue";
import Menubar from "@/components/Header/Menubar.vue";
import Navbar from "@/components/Header/Navbar.vue";
import { useRouter } from "vue-router";
</script>

<style scoped>
.main {
  box-shadow: inset 0 0 20px red;
}
</style>

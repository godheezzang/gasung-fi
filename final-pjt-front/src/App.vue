<script setup>
import { RouterLink, RouterView } from "vue-router";
import "@/assets/main.css";
</script>

<template>
  <!-- <RouterLink :to="{ name: 'home' }">main</RouterLink> -->
  <div class="container">
    <RouterView />
  </div>
</template>

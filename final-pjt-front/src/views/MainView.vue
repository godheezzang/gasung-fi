<template>
  <div class="main">
    <h1 class="title">Main</h1>
    <RouterView />
  </div>
</template>

<script setup>
import { ref } from "vue";
import { RouterView } from "vue-router";
</script>

<style scoped></style>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import "@/assets/main.css";
import Navbar from "@/components/Header/Navbar.vue";
import Menubar from "@/components/Header/Menubar.vue";
</script>

<template>
  <!-- <RouterLink :to="{ name: 'home' }">main</RouterLink> -->

  <div class="container">
    <nav>
      <Navbar />
      <Menubar />
    </nav>
    <main>
      <RouterView />
    </main>
  </div>
</template>

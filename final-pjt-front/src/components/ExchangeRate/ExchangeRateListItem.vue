<template>
  <div>
    <div class="card-title">
      <p>
        {{ rate.country }} <span>{{ rate.cur_unit }}</span>
      </p>
    </div>
    <div>
      <p>
        <span>{{ rate.bkpr }}</span> {{ rate.money }}
      </p>
    </div>

    {{}}
    <!-- {{ rate }} -->
  </div>
</template>

<script setup>
const props = defineProps({
  rate: Object,
});

console.log(props.rate);
</script>

<style scoped></style>

<template>
  <div class="card-container">
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

// console.log(props.rate);
</script>

<style scoped>
.card-container {
  text-align: center;
}

.card-title {
  font-size: var(--font-size-mlarge);
  font-weight: var(--font-weight-medium);
}
</style>

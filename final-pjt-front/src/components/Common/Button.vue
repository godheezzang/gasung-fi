<template>
  <button @click="handleClick" :aria-label="ariaLabel" :class="['btn', 'default-btn', customClass]">
    {{ content }}
  </button>
</template>

<script setup>
const props = defineProps({
  content: String,
  onClick: Function,
  ariaLabel: String,
  customClass: String,
});

const handleClick = () => {
  if (props.onClick) {
    props.onClick();
  }
};
</script>

<style scoped>
.default-btn {
  color: var(--color-white);
  background-color: var(--color-black);
}

.disabled-btn {
  background-color: var(--color-gray-04);
  color: var(--color-gray-01);
  cursor: not-allowed;
}

.small-btn {
  font-size: var(--font-size-extra-small);
  padding: 0.5rem 1rem;
  border-radius: 0.8rem;
}

.large-btn {
  font-size: var(--font-size-mlarge);
  padding: 1rem 2rem;
}
</style>

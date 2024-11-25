<script setup>
const props = defineProps({
  show: Boolean,
});
</script>

<template>
  <Transition name="modal">
    <div v-if="show" class="modal-mask">
      <div class="modal-container">
        <div class="modal-header">
          <slot name="header">default header</slot>
        </div>

        <div class="modal-body">
          <slot name="body">default body</slot>
        </div>

        <div class="modal-footer">
          <slot name="footer">
            <button class="modal-default-button" @click="$emit('close')">
              확인
            </button>
            <button class="modal-default-button" @click="$emit('close')">
              취소
            </button>
          </slot>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  transition: opacity 0.3s ease;
}

.modal-container {
  width: 300px;
  margin: auto;
  padding: 1rem 2rem;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
}

.modal-header h3 {
  color: var(--color-black);
  margin-top: 1rem;
  text-align: center;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--color-gray-02);
  font-size: var(--font-size-mlarge);
  font-weight: var(--font-weight-medium);
}

.modal-body {
  margin: 20px 0;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: space-around;
}

.modal-footer button {
  flex-grow: 1;
  padding: 1rem 2rem;
  border-radius: 5px;
}

button:hover {
  background-color: var(--color-gray-02);
}

.modal-enter-from {
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>

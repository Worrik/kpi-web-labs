<template>
  <Transition name="slide-fade">
    <div v-if="show" class="warning-message">
      <slot></slot>
    </div>
  </Transition>
</template>

<script setup lang="ts">
defineProps<{
  show: boolean
}>()
</script>

<style scoped>
.warning-message {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #fff3cd;
  color: #856404;
  padding: 1rem 2rem;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 9999;
  text-align: center;
  min-width: 200px;
}

.slide-fade-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -30px);
}
</style> 
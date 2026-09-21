<template>
  <div :class="['inline-flex items-center', containerClass]">
    <img 
      :src="logoSrc" 
      :alt="alt" 
      :class="['object-contain select-none transition-all duration-200', imgClass]" 
    />
  </div>
</template>

<script setup>
import logoSrc from '@/assets/logo.png';

defineProps({
  alt: {
    type: String,
    default: 'CareerPilot AI'
  },
  imgClass: {
    type: String,
    default: 'h-9.5 w-auto max-w-[190px]'
  },
  containerClass: {
    type: String,
    default: ''
  }
});
</script>

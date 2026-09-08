<template>
  <div class="student-layout">
    <StudentHeader />
    <div class="layout-body">
      <StudentSidebar />
      <main class="main-content">
        <slot></slot>
      </main>
    </div>
    <AppToast />
  </div>
</template>

<script setup>
import StudentHeader from './StudentHeader.vue'
import StudentSidebar from './StudentSidebar.vue'
import AppToast from '@/components/common/AppToast.vue'
</script>

<style scoped>
.student-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--background);
}

.layout-body {
  display: flex;
  flex: 1;
}

.main-content {
  flex: 1;
  padding: 1.5rem 2rem;
  max-width: 1400px;
  width: 100%;
}
</style>

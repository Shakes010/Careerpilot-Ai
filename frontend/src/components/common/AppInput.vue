<template>
  <div class="form-group">
    <label v-if="label" :for="id" class="form-label">
      {{ label }}
      <span v-if="required" class="required-asterisk">*</span>
    </label>

    <div class="input-wrapper">
      <input
        :id="id"
        :type="computedType"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        class="form-input"
        :class="{ 'has-error': error }"
        @input="$emit('update:modelValue', $event.target.value)"
      />
      <button
        v-if="type === 'password'"
        type="button"
        class="toggle-password-btn"
        @click="showPassword = !showPassword"
      >
        {{ showPassword ? 'Hide' : 'Show' }}
      </button>
    </div>

    <span v-if="error" class="form-error">{{ error }}</span>
    <span v-else-if="hint" class="form-hint">{{ hint }}</span>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  label: { type: String, default: '' },
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  id: { type: String, default: () => `input-${Math.random().toString(36).substring(2, 9)}` },
  required: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  error: { type: String, default: '' },
  hint: { type: String, default: '' }
})

defineEmits(['update:modelValue'])

const showPassword = ref(false)

const computedType = computed(() => {
  if (props.type === 'password') {
    return showPassword.value ? 'text' : 'password'
  }
  return props.type
})
</script>

<style scoped>
.required-asterisk {
  color: var(--danger);

}
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.toggle-password-btn {
  position: absolute;
  right: 0.75rem;
  background: none;
  border: none;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--primary);
  cursor: pointer;
}
.form-hint {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: 0.25rem;
}
.has-error {
  border-color: var(--danger) !important;
}
</style>

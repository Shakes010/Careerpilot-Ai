<template>
  <div class="form-group">
    <label v-if="label" :for="id" class="form-label">
      {{ label }}
      <span v-if="required" class="required-asterisk">*</span>
    </label>

    <select
      :id="id"
      :value="modelValue"
      :disabled="disabled"
      class="form-select"
      :class="{ 'has-error': error }"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option v-if="placeholder" value="" disabled selected>{{ placeholder }}</option>
      <option
        v-for="opt in options"
        :key="opt.value ?? opt"
        :value="opt.value ?? opt"
      >
        {{ opt.label ?? opt }}
      </option>
    </select>

    <span v-if="error" class="form-error">{{ error }}</span>
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: [String, Number], default: '' },
  label: { type: String, default: '' },
  options: { type: Array, required: true }, // [{ label: 'Option', value: 'opt' }] or ['opt1', 'opt2']
  placeholder: { type: String, default: '' },
  id: { type: String, default: () => `select-${Math.random().toString(36).substring(2, 9)}` },
  required: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  error: { type: String, default: '' }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.required-asterisk {
  color: var(--danger);
}
.has-error {
  border-color: var(--danger) !important;
}
</style>

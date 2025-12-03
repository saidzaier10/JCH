<template>
  <div class="w-full">
    <Listbox :model-value="modelValue" @update:model-value="value => $emit('update:modelValue', value)" :disabled="disabled">
      <div class="relative mt-1">
        <ListboxLabel v-if="label" class="block text-sm font-medium text-gray-700 mb-1">
          {{ label }}
        </ListboxLabel>
        <ListboxButton
          class="relative w-full cursor-default rounded-lg bg-white py-3 pl-4 pr-10 text-left border border-gray-300 shadow-sm focus:outline-none focus-visible:border-judo-blue focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-judo-blue sm:text-sm transition-all duration-200"
          :class="{ 'bg-gray-100 text-gray-500 cursor-not-allowed': disabled, 'border-red-300 text-red-900 focus:ring-red-500': error }"
        >
          <span class="block truncate" :class="{ 'text-gray-400': !modelValue }">
            {{ selectedLabel || placeholder }}
          </span>
          <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
            <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
          </span>
        </ListboxButton>

        <transition
          leave-active-class="transition duration-100 ease-in"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <ListboxOptions
            class="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm z-50"
          >
            <ListboxOption
              v-for="option in options"
              v-slot="{ active, selected }"
              :key="option.value"
              :value="option.value"
              as="template"
            >
              <li
                :class="[
                  active ? 'bg-judo-blue/10 text-judo-blue' : 'text-gray-900',
                  'relative cursor-default select-none py-2 pl-10 pr-4',
                ]"
              >
                <span
                  :class="[
                    selected ? 'font-medium' : 'font-normal',
                    'block truncate',
                  ]"
                >
                  {{ option.label }}
                </span>
                <span
                  v-if="selected"
                  class="absolute inset-y-0 left-0 flex items-center pl-3 text-judo-blue"
                >
                  <CheckIcon class="h-5 w-5" aria-hidden="true" />
                </span>
              </li>
            </ListboxOption>
          </ListboxOptions>
        </transition>
      </div>
    </Listbox>
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  Listbox,
  ListboxLabel,
  ListboxButton,
  ListboxOptions,
  ListboxOption,
} from '@headlessui/vue'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  options: {
    type: Array,
    required: true,
    // Expected format: [{ label: 'Label', value: 'value' }]
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Sélectionner...',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
})

defineEmits(['update:modelValue'])

const selectedLabel = computed(() => {
  const option = props.options.find((o) => o.value === props.modelValue)
  return option ? option.label : ''
})
</script>

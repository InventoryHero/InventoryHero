<script setup lang="ts">
import useAppStyling from '@/composables/useAppStyling.ts'

type rule = ((value: string) => string | boolean) | boolean | string

const { textFieldStyling } = useAppStyling()
const { t } = useI18n()

const password = defineModel<string>()

const { rules = [] } = defineProps<{
  rules?: Array<rule>
}>()

const visible = ref(false)

const innerIcon = computed(() => {
  if (visible.value) {
    return 'mdi-eye-off'
  }
  return 'mdi-eye'
})

function showPassword() {
  visible.value = !visible.value
}
</script>

<template>
  <v-text-field
    v-bind="{
      ...textFieldStyling,
      ...$attrs
    }"
    :type="visible ? 'text' : 'password'"
    v-model="password"
    :rules="rules"
    :append-inner-icon="innerIcon"
    @click:append-inner="showPassword"
  >
    <template v-slot:message="{ message }">
      <template v-if="message === 'weak'">
        <div class="password-feedback">
          <p>
            <strong>{{ t('validation.password.weak.title') }}</strong>
            {{ t('validation.password.weak.subtitle') }}
          </p>
          <ul class="indented-list">
            <li>
              {{ t('validation.password.weak.num_characters') }}
            </li>
            <li>
              {{ t('validation.password.weak.lower_case') }}
            </li>
            <li>
              {{ t('validation.password.weak.upper_case') }}
            </li>
            <li>
              {{ t('validation.password.weak.number') }}
            </li>
            <li>
              {{ t('validation.password.weak.symbol') }}
            </li>
          </ul>
        </div>
      </template>
      <template v-else>
        {{ message }}
      </template>
    </template>
  </v-text-field>
</template>

<style scoped lang="scss">
.password-feedback {
  font-size: 0.85rem;
  line-height: 1.4;

  ul {
    padding-left: 1.5rem;
    margin: 0.25rem 0 0;
    list-style-type: disc;

    li {
      margin-bottom: 0.15rem;
      position: relative;
      padding-left: 1.25rem;
    }
  }
}
</style>

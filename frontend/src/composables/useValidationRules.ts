import validator from 'validator'

export default (password: Ref<string | undefined | null>) => {
  const { t } = useI18n()

  const usernameRules = ref([
    (value: string | undefined | null) =>
      !!value || t('validation.username.required'),
    (value: string) => value.length >= 3 || t('validation.username.too_short'),
    (value: string) => value.length <= 256 || t('validation.username.too_long'),
    (value: string) =>
      validator.isAlphanumeric(value) ||
      t('validation.username.invalid_characters')
  ])

  const emailRules = ref([
    (value: string | undefined | null) =>
      !!value || t('validation.email.required'),
    (value: string) =>
      validator.isEmail(value) || t('validation.email.invalid_email')
  ])

  // TODO PASSWORD VALIDATION
  const passwordRules = ref([
    (value: string | undefined | null) =>
      !!value || t('validation.password.required')
  ])

  const passwordRepeatRules = ref([
    (value: string | undefined | null) =>
      !!value || t('validation.repeat_password.required'),
    (value: string) =>
      value === password.value ||
      t('validation.repeat_password.password_mismatch')
  ])

  return {
    usernameRules,
    emailRules,
    passwordRules,
    passwordRepeatRules
  }
}

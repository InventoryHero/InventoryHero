export default (inviteLink: Ref<string>, householdName: Ref<string>) => {
  const { t } = useI18n()

  const copiedConfirm = ref(false)
  const copyToClipboardIcon = ref('mdi-clipboard-outline')
  const webShareApiSupported = computed(() => !!navigator.share)

  const whatsAppShare = computed(() => {
    return {
      text: inviteLink.value
    }
  })

  const emailShare = computed(() => {
    return {
      subject: t('invite.email.subject', { household: householdName.value }),
      body: t('invite.text', { inviteLink: inviteLink.value }),
      mail: ''
    }
  })

  const navigatorShare = () => {
    navigator.share({
      title: t('invite.email.subject', { household: householdName.value }),
      text: t('invite.text'),
      url: inviteLink.value
    })
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(inviteLink.value)
    copyToClipboardIcon.value = 'mdi-check-bold'
    setTimeout(() => {
      copyToClipboardIcon.value = 'mdi-clipboard-outline'
    }, 2000)
    return
  }

  return {
    webShareApiSupported,
    copyToClipboardIcon,
    emailShare,
    whatsAppShare,
    navigatorShare,
    copyToClipboard
  }
}

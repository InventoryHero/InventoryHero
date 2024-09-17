
export default (inviteLink: Ref<string>, householdName: Ref<string>) =>{
    const {t} = useI18n()

    const copiedConfirm = ref(false)

    const webShareApiSupported = computed(() => navigator.share)

    const whatsAppShare = computed(() => {
        return {
            text: inviteLink.value
        }
    })

    const emailShare = computed(() => {
        return {
            subject: t('invite.email.subject', {household: householdName.value}),
            body: t('invite.text', {inviteLink: inviteLink.value}),
            mail: ""
        }
    })

    const navigatorShare = () => {
        navigator.share({
            title: t('invite.email.subject', {household: householdName.value}),
            text: t('invite.text'),
            url: inviteLink.value
        })
    }

    const copyToClipboard = () => {
        navigator.clipboard.writeText(inviteLink.value);
        copiedConfirm.value = true;
        return
    }

    return {
        webShareApiSupported,
        copiedConfirm,
        emailShare,
        whatsAppShare,
        navigatorShare,
        copyToClipboard
    }
}
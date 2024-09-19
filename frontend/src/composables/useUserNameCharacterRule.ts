
export default () => {
    const {t} = useI18n()

    const usernameCharacterRule = (value: string): boolean | string => {
        const usernameRegex = /^[a-zA-Z0-9._-]{3,25}$/;
        if (!usernameRegex.test(value)) {
            return t('rules.username_fmt_rule');
        }
        return true;
    };

    return {
        usernameCharacterRule
    };
}

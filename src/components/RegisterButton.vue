<template>
<div class="containerLoginButton">
    <button>{{ this.$t('login_view.register') }}</button>
</div>
</template>

<script>
export default {
name: 'LoginButton',
}
</script>

<style scoped>
button {
    width: 20vw;
    height: 10vw;
    font-size: 1em;
    border-radius: 10px;
    border: none;
    background-color: var(--color-dark-theme-lighter);
    color: white;
}
</style>
  
  
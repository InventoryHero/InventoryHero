<template>
  <div class="containerInputText">
    <input v-if="this.is_pssw == false" :placeholder=this.place_holder type="text" v-model="this.my_value" @input="$emit('valueUpdated', this.my_value)">
    <input v-else :placeholder=this.place_holder type="password" v-model="this.my_value" @input="$emit('valueUpdated', this.my_value)">
  </div>
</template>

<script>
export default {
  name: 'InputText',
  props: ["place_holder", "is_pssw"],
  data() {
    return {
      my_value: ""
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
input {
  background-color: var(--color-darker);
  color: white;
  width: 60%;
  font-size: 1.5em;
  padding: 20px;
  border: none;
  border-radius: 15px;
}

::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
  color: var(--color-faded);
}
:-ms-input-placeholder { /* Internet Explorer 10-11 */
  color: var(--color-faded);
}
::-ms-input-placeholder { /* Microsoft Edge */
  color: var(--color-faded);
}

input:focus {
  outline: none;
}
</style>

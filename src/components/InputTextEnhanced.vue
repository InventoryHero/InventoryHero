<template>
    <input :disabled="this.disabled" :placeholder=this.place_holder type="text" v-model="this.my_value" @input="$emit('valueUpdated', this.my_value)">
</template>

<script>
export default {
  name: 'InputText',
  props: {
      place_holder: {
          type: String,
          default: ""
      },
      disabled: {
          type: Boolean,
          default: false
      }
  },
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
  color: white;
  font-size: 1.5em;
  padding-left: 20px;
  padding-top: 5px;
  padding-bottom: 5px;
  border: none;
  width: 100%;
  border-radius: 15px;
  border: 1px solid white;
  margin-bottom: 10px;
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

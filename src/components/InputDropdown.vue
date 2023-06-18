<template>
  <div id="mainSelector">
      <select :disabled="this.isSelectDisabled()" v-model="this.my_value" @change="this.emitValueChanged()">
          <option hidden disabled selected>{{ this.place_holder }}</option>
          <option  v-bind:value="l" v-for="l in this.list" :key="l.key">{{ l.name }} </option>
      </select>
    </div>
</template>

<script>
export default {
  name: 'InputText',
  props: {
    place_holder: String,
    list: Array,
    isDisabled: {
      type: Boolean,
      default: false,
    },
    id: String,
    emitFullObject: {
      type: Boolean,
      default: false,
    }
  },
  watch: {
    place_holder: function(newVal, oldval)
    {
      this.my_value = newVal;
    }
  },
  data() {
    return {
      my_value: this.place_holder,
    }
  },
  methods: {
    emitValueChanged(){
      if(this.emitFullObject)
        this.$emit("valueUpdated", this.my_value);
      else
        this.$emit("valueUpdated", this.my_value.name);
    },
    isSelectDisabled()
    {
      return this.isDisabled;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
select {
  color: var(--color-faded);
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

select:focus {
  outline: none;
}
</style>

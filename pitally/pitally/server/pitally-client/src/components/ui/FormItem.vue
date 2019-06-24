<template functional>
  <label>
    <span class="db gray">{{props.label}}</span>
    <slot/>
  </label>
</template>

<script>
export default {

}
</script>

<style scoped>
.fields {
  display: grid;
  grid-gap: 1.2rem;
}
</style>


<template>
  <div class>
   <pre v-if='$store.$data.devMode != "production"' class="absolute z-2 top-0">{{ $store.$data }}</pre>
  <div class="pa4">
  <v-btn>Restart server</v-btn>
  <v-btn>Update </v-btn>
  
  </div>
   </div>

</template>

<script>
</script>
<style scoped>
</style>

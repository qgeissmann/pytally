<template>
  <div id="app">
    <v-app>
        <v-toolbar>
    <v-toolbar-title>{{ $store.$data.deviceInfo.id }} ({{ $store.$data.deviceInfo.status }})</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items class="hidden-sm-and-down">
      <v-btn href='/#/' flat>Devices</v-btn>
      <v-btn href='/#/video_lib' flat>Video library</v-btn>
      <v-btn href='/#/photo_lib' flat>Photo library</v-btn>
      <!-- <v-btn href='/#/manage' flat>Manage</v-btn> -->
    </v-toolbar-items>
  <v-toolbar-side-icon></v-toolbar-side-icon>
    
  </v-toolbar>

      <router-view/>
    </v-app>
  </div>
</template>


<script>
export default {
  name: 'app',
  components: {
  },
  data: () => ({

  }),
  methods: {

  }
}
</script>

<style>
#app {
  font-family: Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>

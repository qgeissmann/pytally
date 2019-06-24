<template>
  <div class>
    <v-btn
        type="submit"
        color="primary"
        @click="$store.makeVideoLibrary"
        :loading="$store.loadings.isMakingVideoLib"
      >
        <v-icon left>refresh</v-icon>Refresh library
      </v-btn>

  <VideoLibrary/>
   </div>

</template>

<script>
import VideoLibrary from '../VideoLibrary'

export default {
  name: 'VideoLibRoute',
  components: {
    VideoLibrary
  },
  data: () => ({

  }),
}
</script>
<style scoped>
</style>

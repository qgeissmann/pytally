<template>
  <v-data-table
    v-model="$store.selectedImgs"
    :headers="headers"
    :items="imagesData"
    item-key="filename"
    select-all
  >
    <template slot="items" slot-scope="props">
      <td>
        <v-checkbox v-model="props.selected" primary hide-details></v-checkbox>
      </td>
      <td>{{ props.item.filename }}</td>
      <td>
        <img :src="props.item.image" width="100">
      </td>
    </template>
  </v-data-table>
</template>
<script>
export default {
  name: 'ImageTable',
  data: () => ({
    headers: [
      { text: 'Name', value: 'filename' },
      { text: 'Preview', value: 'image' },
    ]
  }),
  computed: {
    imagesData() {
      return this.$store.images
    }
  }
}
</script>
<style scoped>
</style>


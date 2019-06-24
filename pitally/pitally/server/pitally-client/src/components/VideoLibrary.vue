<template>
  <v-data-table
    v-model="$store.videoLibrary"
    :headers="headers"
    :items="$store.videoLibrary"
    item-key="hostname"
    select-all
  >
    <template slot="items" slot-scope="props">
      <td>
        <v-checkbox v-model="props.item.selected" primary hide-details></v-checkbox>
      </td>
      <td>{{ props.item.device}}</td>
      <td>{{ props.item.datetime }}</td>

      <td>
        <a :href="props.item.link"  width="33">{{ props.item.prefix }} </a>
        </td>

      <td>{{ props.item.format }}</td>
      <td>{{ props.item.end }}</td>
    </template>

  </v-data-table>
</template>
<script>
export default {  
  name: 'videoLibrary',
  data: () => ({
    headers: [
      { text: 'Device', value: 'device'},
      { text: 'Date', value: 'datetime'},  
      { text: 'Name', value: 'prefix'},
      { text: 'Format', value: 'format'},
      { text: 'Chunks', value: 'end'},
    ]
  }),
}
</script>
<style scoped>
</style>


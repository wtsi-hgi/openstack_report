<template>
  <div id="app" class = "small-container">
    <nav> </nav>
    <b-alert variant="success" show> Last updated at: {{lastUpdated}}</b-alert>
    <report-table v-bind:clusters="clusters" />
  </div>

</template>

<script>
import ReportTable from '@/components/ReportTable.vue'
import Nav from '@/components/Nav.vue'


export default {
  name: 'app',

  components: {
    ReportTable,
    Nav
  },

  data(){
   return {
      clusters: [],
      lastUpdated: null
    }
  },

  mounted(){
    this.getClusters()
  },

  methods: {

    async getClusters(){
      try {
        const response = await fetch(process.env.VUE_APP_BACKEND_API_URL + '/report')        
        const wholeResponse = await response.json()
        this.clusters = wholeResponse.data
        this.lastUpdated = wholeResponse.time
      } catch (error) {
        console.error(error)
      }
    },
   }
}

</script>


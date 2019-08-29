<template>
  <div id="app" class = "small-container">
<!--     <img alt="Vue logo" src="./assets/logo.png"> -->
   <!--  <HelloWorld msg="Welcome to Your Vue.js App"/> -->
   <!--  <h1>Hail Clusters</h1> -->
  <!--   <test-form @add:cluster="addCluster" /> -->

    <nav> </nav>
 
    
    <b-alert variant="success" show> Last updated at: {{lastUpdated}}</b-alert>
    
    <report-table v-bind:clusters="clusters" />
    <!-- <refresh-button @refresh:clusters="refreshClusters"/> -->
  </div>

</template>


<script>


import ReportTable from '@/components/ReportTable.vue'
import Nav from '@/components/Nav.vue'
// import RefreshButton from '@/components/RefreshButton.vue'
// import TestForm from '@/components/TestForm.vue'


export default {
  name: 'app',
  components: {
   
    ReportTable,
    Nav,
    // RefreshButton
    // TestForm,
  },
  data(){

   return {
      clusters: [],
      lastUpdated: null
    }
  },

  mounted(){
    console.log("Sending request to fetch clusters")
    this.getClusters()
  },
  methods: {

    async getClusters(){
      try{
  
        const response = await fetch('http://172.27.83.209:8082/report')     
        const wholeResponse = await response.json()
        this.clusters = wholeResponse.data
        this.lastUpdated = wholeResponse.time
      } catch (error) {
        console.error(error)
      }
    },

     async refreshClusters(){
      try{
  
        const response = await fetch('http://localhost:8081/refresh')     
        const wholeResponse = await response.json()
        this.clusters = wholeResponse.data
        this.lastUpdated = wholeResponse.time
      } catch (error) {
        console.error(error)
      }
    },

    // addCluster(cluster){
    //   const lastId = this.employees.length > 0 ? this.cluster[this.cluster.length-1].id :0;
    //   const id = lastId + 1
    //   const newCluster = {...cluster, id}
    //   this.clusters = [...this.clusters, cluster]
    // },

    async getCpuHours(user_name){

      try {
        var url = new URL("http://localhost:8081/report/cpu/time")
        var params = {'user_name': user_name }
        url.search = new URLSearchParams(params)
        console.log("fetch request: " + JSON.stringify(url))
        var response = await fetch(url)
        // var params = {method: 'POST', body: JSON.stringify(server_names), headers: {'Accept': 'application/json', 'Content-Type': 'application/json'}}
        // const response = await fetch("http://localhost:8081/report/cpu/time", params)// 
        const data = await response.json()

        for (var cluster of this.clusters){
          if (cluster['user_name'] == name){
            cluster['cpu_hours'] = data
             break;
          }
        }
      } catch (error){
        console.error(error)
      }
    }
   }
}

</script>

<!-- <style>
/*  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">*/
/*#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}*/

/*button {
   background: #009435;
  border: 1px solid #009435;
}

.small-container {
  max-width: 680px;
}*/
</style>
 -->
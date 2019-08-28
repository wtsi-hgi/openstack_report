

<template>
	
	<div id = "report-table">
	
		<b-table  :fields="fields" :items="clusters">		
		</b-table>

	
	</div>

	
</template>


<script>
	export default {
		name: 'report-table',
		props: {
			clusters: Array,
		},
		data(){
			return {

				loading: false,

				fields:[
					{
						key: 'user_name',
						label: "User",
						sortable: false

					},

					{
						key: 'master',
						label: 'Master Nodes',
						sortable: true

					},

					{
						key: 'slaves',
						label: "Slave Nodes",
						sortable: true

					},

					{
						key: 'cores',
						label: "Total Cores",
						sortable: true

					},

					{
						key: 'created_date',
						label: "Created At",
						sortable: true
					},

					{
						key: 'cpu_hours',
						label: "CPU Hours",
						sortable: true

					},

					{
						
						label: "Actions",
						sortable: false

					}
						
				]
			}

		},

		created() {
		
		},

		watch: {



		},

		methods: {

		

		}


	}
</script>

<!-- <style scoped> </style> -->





<template>
	
	<div id = "refresh_button">

		<b-button  type="submit" block variant="primary"  v-on:click="$emit('refresh:clusters')">
			<b-spinner v-if="loading" small type="grow"></b-spinner>
			Fetch latest report
		</b-button>
	
	</div>

	
</template>


<script>
	export default {
		name: 'refresh_button',
		
		data(){
			return {

				loading: false,
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



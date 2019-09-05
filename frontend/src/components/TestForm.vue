<template>
	<div id = "test-form">
		<form @submit.prevent = "handleSubmit">
			<label>User name</label>
			<input 
				v-model= "cluster.name" 
				ref= "first"
				type="text"
				:class = "{'has-error':submitting && invalidName}"
				@focus="clearStatus"
				@keypress="clearStatus"/>
			<label>master</label>
			<input 
				v-model= "cluster.master" 
				type="text"
				@focus="clearStatus"/>
			<p v-if="error && submitting" class = "error-message">
				!Please fill out all required fields
			</p>
			<p v-if="success" class="success-message">
				Cluster successfully added
			</p>	
			<button>Add Cluster</button>
		</form>
	</div>
</template>


<script>
	export default {
		name: 'test-form',
		data(){
			return {
				cluster: {
					name: '',
					master: ''
				},
				submitting: false,
				error: false,
				success: false
			}
		},
		methods: {
			handleSubmit(){
				console.log('testing handleSubmit')
				this.submitting = true
				this.clearStatus()
				if (this.invalidName){
					this.error = true
					return
				}
				this.$emit('add:cluster', this.cluster)
				this.$refs.first.focus()
				this.cluster = {
					name: '',
					master: ''
				}
				this.success = true
				this.submitting = false
				this.error = false
			},
			clearStatus(){
				this.success = false
				this.error = false
			}
		},
		computed: {
			invalidName() {
				return this.cluster.name === ''
			},

		}
	}
</script>


<style scoped>
	form {
		margin-bottom: 2rem
	}

	[class*= '-message']{
		font-weight: 500;
	}

	.error-message {
		color: #32a95d;
	}

	.success-message {
		color: #32a95d;
	}
</style>
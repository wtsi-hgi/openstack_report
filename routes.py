




import controller


def load_routes(app):
	app.router.add_get('/report', controller.get_report)
	# app.router.add_get('/refresh', controller.refresh_report)
	# app.router.add_get('/report/cpu/time', controller.get_cpu_time)

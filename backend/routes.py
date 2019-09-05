




import controller


def load_routes(app):
	app.router.add_get('/api/report', controller.get_report)


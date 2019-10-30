module.exports = {
    publicPath: "/cluster-report/",
    devServer: { 
    	disableHostCheck: true,
    	public: "http://apps.hgi.sanger.ac.uk/cluster-report/",
    	proxy: {
        "/sockjs-node": {
            	target: "http://localhost:8080/cluster-report",
            	pathRewrite: { "^/sockjs-node": "/cluster-report/sockjs-node" },
        	},
    	}
    } 
}

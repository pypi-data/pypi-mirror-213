module.exports = {
    lintOnSave: false,
    devServer: {
        disableHostCheck: true,
        host: "0.0.0.0",
        port: 8081,
        proxy: {
            "": {
                target: "http://127.0.0.1:17310/",
                ws: true,
                changeOrigin: true,
            },
        }
    },
    assetsDir: 'static',
}

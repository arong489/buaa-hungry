const {
    defineConfig
} = require('@vue/cli-service')

module.exports = defineConfig({
    lintOnSave: false,
    transpileDependencies: true,
    devServer: {
        host: 'localhost',
        port: 8080, //没被占用，可以使用的端口
        open: true,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000/',
                changeOrigin: true,
                ws: true, // 是否代理 websockets
                pathRewrite: { // 路径重置
                    '^/api': ''
                }
            }
        }
    }
})

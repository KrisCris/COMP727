module.exports = {
    "transpileDependencies": [
        "vuetify"
    ],
    devServer: {
        proxy: 'http://192.168.123.98:5000',
        disableHostCheck: true,
    },
}
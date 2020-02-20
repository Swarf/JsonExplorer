'use strict';

const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const path = require('path');
const distPath = path.resolve(__dirname, 'dist');

module.exports = {
    entry: {
        app: './src/index.js',
    },
    output: {
        filename: 'js/[name].js',
        path: distPath,
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    "style-loader",
                    "css-loader"
                ]
            },
            {
                test: /\.(ico|jpe?g|png|gif)$/,
                loader: "file-loader"
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin(),
        new HtmlWebpackPlugin({
            title: 'Json Explorer',
        }),
    ],
    // mode: 'development',
    devtool: 'source-map',
    devServer: {
        // Display only errors to reduce the amount of output.
        stats: "errors-only",
        contentBase: distPath,
        // publicPath: '/',
    },
};

var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

var config = require('./webpack.base.config.js');

// Use webpack dev server with Hot Replacement Module
config.entry = [
  './assets/js/index'
];

config.output.publicPath = '[name].[hash].js';

config.plugins = config.plugins.concat([
  new webpack.NoEmitOnErrorsPlugin(),
  new webpack.NamedModulesPlugin(),
  new BundleTracker({filename: './webpack-stats.json'}),
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify("production")
    }
  }),
  new webpack.optimize.UglifyJsPlugin({
    minimize: true,
    compress: true
  })
]);

config.devtool = 'eval';

// Add a loader for JSX files with react-hot enabled
config.module.loaders.push(
  {
    test: /\.js?$/,
    exclude: /node_modules/,
    loaders: [
      'babel-loader?presets[]=es2015,presets[]=stage-0,presets[]=react'
    ],
  }
);

module.exports = config;

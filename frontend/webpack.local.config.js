var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

var config = require('./webpack.base.config.js');

// Use webpack dev server with Hot Replacement Module
config.entry = [
  'react-hot-loader/patch',
  'webpack-dev-server/client?http://localhost:4000',
  'webpack/hot/only-dev-server',
  './assets/js/index'
];

// override django's STATIC_URL for webpack bundles
config.output.publicPath = 'http://localhost:4000/assets/bundles/';

config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoEmitOnErrorsPlugin(),
  new webpack.NamedModulesPlugin(),
  new BundleTracker({filename: './webpack-stats.json'}),
]);

config.devtool = 'eval';

// Add a loader for JSX files with react-hot enabled
config.module.loaders.push(
    {
      test: /\.js?$/,
      exclude: /node_modules/,
      loaders: [
        'react-hot-loader/webpack',
        'babel-loader?presets[]=es2015,presets[]=stage-0,presets[]=react'
      ],
    }
);

module.exports = config;

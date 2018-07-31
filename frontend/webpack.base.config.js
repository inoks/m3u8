var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,
  entry: './assets/js/index',
  output: {
    path: path.resolve('./assets/bundles/'),
    filename: "bundle.js",
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'})
  ], // add all common plugins here
  module: {
    loaders: [] // add all common loaders here
  },
  resolve: {
    modules: ['node_modules', 'bower_components'],
    extensions: ['.js', '.jsx']
  },
};

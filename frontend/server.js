var webpack = require('webpack');
var WebpackDevServer = require('webpack-dev-server');
var config = require('./webpack.local.config');

new WebpackDevServer(webpack(config), {
  stats: {
    colors: true
  },
  disableHostCheck: true,
  headers: {"Access-Control-Allow-Origin": "*"},
  historyApiFallback: true,
  hot: true,
  inline: true,
  publicPath: config.output.publicPath
}).listen(4000, '0.0.0.0', function (err, result) {
  if (err) {
    console.log(err)
  }
  console.log('Listening at 0.0.0.0:4000')
});

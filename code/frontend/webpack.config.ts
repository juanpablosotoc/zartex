const path = require('path');
const TsconfigPathsPlugin = require('tsconfig-paths-webpack-plugin');


module.exports = {
  // … your existing config …
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx', '.scss', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg'],
    alias: {
      '@myImages':    path.resolve(__dirname, 'src/assets/images'),
      '@myComponents': path.resolve(__dirname, 'src/components'),
      '@myPages':      path.resolve(__dirname, 'src/pages')
    }
    // you can leave TsconfigPathsPlugin here if you want, but alias covers it
  },
  module: {
    rules: [
      // ts-loader, css, assets, etc.
    ]
  }
};
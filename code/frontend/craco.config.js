// craco.config.js
const path = require('path');

module.exports = {
  webpack: {
    alias: {
      '@myImages':     path.resolve(__dirname, 'src/assets/images'),
      '@myComponents': path.resolve(__dirname, 'src/components'),
      '@myPages':      path.resolve(__dirname, 'src/pages'),
      '@myIcons':      path.resolve(__dirname, 'src/assets/icons'),
    }
  }
};

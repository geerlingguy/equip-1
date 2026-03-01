module.exports = {
  apps: [
    {
      name: 'equip-1',
      script: '.output/server/index.mjs',
      env: {
        NODE_ENV: 'production',
        PORT: 3234
      }
    }
  ]
}

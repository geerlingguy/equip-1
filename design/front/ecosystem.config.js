module.exports = {
  apps: [
    {
      name: 'front',
      script: '.output/server/index.mjs',
      instances: 'max',
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'production',
        PORT: 3234;
      }
    }
  ]
}

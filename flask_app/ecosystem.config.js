module.exports = {
  apps: [
    {
      name: 'flight_agent_back',
      script: 'python3',
      args: '-m flask run --host=127.0.0.1 --port=5000 --cert=/etc/letsencrypt/live/weezle.co/fullchain.pem --key=/etc/letsencrypt/live/weezle.co/privkey.pem --debugger',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        FLASK_ENV: 'dev',
        FLASK_APP: 'main.py'
      },
      env_production: {
        FLASK_ENV: 'prod',
        FLASK_APP: 'main.py'
      }
    }],

  deploy: {}
};

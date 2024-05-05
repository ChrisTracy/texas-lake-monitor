# Texas Lake Level Alert

This project comes as a pre-built docker image that scrapes waterdatafortexas.org and sends a pushover alert if the lake level changes.

1. Create a docker-compose.yml file:
```bash
nano docker-compose.yml
```

2. Add this to the YAML file with your own parameters. I am using Lake Weatherford as an example:
```yml
version: '3.8'
services:
  lake-monitor:
    image:  christracy/tx-lake-monitor
    container_name: tx-lake-monitor
    restart: unless-stopped

    environment:
      LAKE_NAME: "weatherford"
      PUSHOVER_APP_TOKEN: "[YOUR PUSHOVER APP TOKEN]"
      PUSHOVER_USER_KEY: "[YOUR  PUSHOVER USER TOKEN]"
      INTERVAL: 21600 #How often (seconds) this will check for changes. Default is 6 hours

    volumes:
      - lake_monitor_volume:/data

volumes:
  lake_monitor_volume:
```

9. Bring up your stack by running:

```bash
docker compose up -d
```
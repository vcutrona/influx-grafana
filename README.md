# Influx + Grafana

This repository deploys a simple environment with InfluxDB (v2.7.4) and Grafana (OSS v11.6.0), using Docker Compose.

It also runs a script that indefinitely sends new data points to InfluxDB every second.
Points represent measurements of chlorine and temperature, which are read from sensors installed in a swimming pool (and tagged with mode = `auto`).
The script also has a small chance of generating "manual" points, simulating manual measurements of chlorine and temperature (tagged with mode = `manual`).

This repository is intended primarily for educational purposes. The data generated is not intended to be accurate.


## How to use

Start the containers with the command:

```bash
docker compose up -d
```

This command will also build a Docker image to run the data generator script from a container.

Access InfluxDB and Grafana from their own Web applications:

- InfluxDB: http://localhost:8086
- Grafana: http://localhost:3000

To stop and remove containers, run the command:

```bash
docker compose down
```

Some named volumes are defined to persist data from containers. To delete named volumes and anonymous volumes attached to containers, run the `down` command with the `-v` option.

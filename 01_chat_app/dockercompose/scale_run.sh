cp -f nginx/default_scale3.conf nginx/default.conf
docker compose up --scale web=3

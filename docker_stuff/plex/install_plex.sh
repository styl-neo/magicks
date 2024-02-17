#!/bin/bash

docker run -d \
  --name=plex \
  --net=host \
  -e PUID=1000 \
  -e PGID=1000 \
  -e VERSION=docker \
  -v /media/storage/plex/config:/config \
  -v /media/storage/plex/data/series:/series \
  -v /media/storage/plex/data/movies:/movies \
  -v /media/storage/plex/data/anime:/anime \
  --restart unless-stopped \
  lscr.io/linuxserver/plex:latest


# zeit-on-tolino
> Sync the latest ZEIT editions (ePub) with Tolino Cloud

## Usage

The following environment variables should be set:
- TOLINO_USER: username/e-mail of Tolino Cloud account
- TOLINO_PASSWORD: password of Tolino Cloud account
- TOLINO_PARTNER: Tolino Partner according to https://github.com/darkphoenix/tolino-calibre-sync
- TOLINO_USE_DEVICE_TOKEN: TRUE to use device token for authentication (TOLINO_USER=hardware_id / TOLINO_PASSWORD=t_auth_token) - more infos: https://github.com/darkphoenix/tolino-calibre-sync#workaround-for-auth-issues
- ZEIT_USER: e-mail of ZEIT account
- ZEIT_PASSWORD: password of ZEIT account
- SCHEDULING: 
  - true: sync at startup + scheduled syncs for wednesday evenings
  - false: one time sync only

docker-compose example:

<pre>
version: '3'

services:
  
  zeitOnTolino:
    image: patrickvogel/zeit-on-tolino:latest
    restart: always
    volumes:
      - ./volumes/zeit-on-tolino/epubs:/var/epubs
    environment:
      SCHEDULING: "true"
      TOLINO_USER: "< TOLINO_CLOUD_USER >"
      TOLINO_PASSWORD: "< TOLINO_CLOUD_PASSWORD >"
      TOLINO_PARTNER: "< TOLINO_PARTNER >"
      TOLINO_USE_DEVICE_TOKEN: "TRUE"
      ZEIT_USER: "< ZEIT_USER >"
      ZEIT_PASSWORD: "< ZEIT_PASSWORD >"
</pre>

## Related libraries

`zeit-on-tolino` uses [`darkphoenix/tolino-calibre-sync`](https://github.com/darkphoenix/tolino-calibre-sync) to connect with Tolino Cloud.
# zeit-on-tolino
> Sync the latest ZEIT editions (ePub) with Tolino Cloud

## Usage

The following environment variables should be set:
- TOLINO_USER: username/e-mail of Tolino Cloud account
- TOLINO_PASSWORD: password of Tolino Cloud account
- TOLINO_PARTNER: Tolino Partner according to https://github.com/hzulla/tolino-python
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
      ZEIT_USER: "< ZEIT_USER >"
      ZEIT_PASSWORD: "< ZEIT_PASSWORD >"
</pre>

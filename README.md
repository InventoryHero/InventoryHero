# InventoryHero

InventoryHero started as an university project for the course "Mobile Applications" at TU Graz. The basic idea was to provide a simple and easy to use inventorying system for home users. It should be easy to use and simplistic in it's design. 

Though after the course ended we noticed a few things off with the initial draft of the app and I started working on it alone besides univeristy and other projects. Staying true to the origins of InventoryHero the frontend is developed in Vue.js (which I started learning with this project) and Python is used for the backend (where I am also still learning and experimenting with this project). 

## Setup 

I am planning to release the docker image into the wild at some point in time, but for now this repo needs to be forked and the image build with the following docker compose (which can also be found in the base of this repository).

This is the minimal docker compose needed for InventoryHero to work. WIth this configuration in memory sqlite database will be used, so it should be good for giving InventoryHero a try.

```
version: "3.4"
services:
  inventoryhero:
    container_name: inventory-hero
    image: inventoryhero
    build:
      target: release
      dockerfile: Dockerfile
    restart: always
    ports:
      - 8080:80
```

The following environment variables are available to configure InventoryHero to your needs. For example database configurations please see [Database](#database)

| Variable                            | Description                                                                                                      |
|-------------------------------------|------------------------------------------------------------------------------------------------------------------|
| INVENTORYHERO_DB_TYPE               | Database type (mysql, postgresql or sqlite)                                                                      |
| INVENTORYHERO_DB_HOST               | Database host                                                                                                    |
| INVENTORYHERO_DB_PORT               | Database port                                                                                                    |
| INVENTORYHERO_DB_NAME               | Database name                                                                                                    |
| INVENTORYHERO_DB_USER               | Database username                                                                                                |
| INVENTORYHERO_DB_PASSWORD           | Database password                                                                                                |
| INVENTORYHERO_APP_URL               | Needed such that confirmation emails have the proper URL set. (Should be the you configured for InventoryHero)   |
| INVENTORYHERO_CONFIRMATION_NEEDED   | States if you want to force email confirmation upon registration                                                 |
| INVENTORYHERO_SECRET_KEY            | JWT_SECRET_KEY used by Flask. Override this!                                                                     |
| INVENTORYHERO_SMTP_FROM_ADDRESS     | The email address InventoryHero should send emails with                                                          |
| INVENTORYHERO_SMTP_FROM_NAME        | The name InventoryHero should send emails with                                                                   |
| INVENTORYHERO_SMTP_SERVER           | The smtp server used to send emails                                                                              |
| INVENTORYHERO_SMTP_USERNAME         | The smtp server username to login to                                                                             |
| INVENTORYHERO_SMTP_PASSWORD         | The smtp server password to login with                                                                           |
| INVENTORYHERO_SMTP_PORT             | The smtp port                                                                                                    |
| INVENTORYHERO_SMTP_PROTOCOL         | The smtp protocol (currently ony SSL is supported)                                                               |
| PGID                                | Group id (docker). Default: 1000                                                                                 |
| PUID                                | User id (docker). Default: 1000                                                                                  |

### Database

<b>WIP<b>

## Credits
Thanks to: 
* My Mobile Application course colleagues and co-creator of InventoryHero: 
    * [Sebastian](https://github.com/Sebastian-debug)
    * [Christian](https://github.com/p4s3r0) - special thanks for creating the InventoryHero icon
    * [Hans-Jürgen](https://github.com/hkleeberger)

* Other OpenSource Projects where I could turn to for implementation (as well as design) guidance:
    * [Fluidd Core](https://github.com/fluidd-core/fluidd)
    * [Spoolman](https://github.com/Donkie/Spoolman)
    * [Vikunja](https://github.com/go-vikunja/vikunja)
    * [Mealie](https://github.com/mealie-recipes/mealie/tree/mealie-next)

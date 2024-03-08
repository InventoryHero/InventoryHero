# InventoryHero

InventoryHero started as an university project for the course "Mobile Applications" at TU Graz. The basic idea was to provide a simple and easy to use inventorying system for home users. It should be easy to use and simplistic in it's design. 

This marks my first "big" project using Vue.js with Vite and Vuetify for frontend and Python Flask for the backend. 

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

The following environment variables are available to configure InventoryHero to your needs: 

|Variable                 | Description                                                   |
|-------------------------|---------------------------------------------------------------|
|DATABASE_URI             | SQL Alchemy Database URI see [database](#database)            |
|APP_URL                  | Needed such that confirmation emails have the proper URL set. (Should be the you configured for InventoryHero)|
|CONFIRMATION_NEEDED      | States if you want to force email confirmation upon registration|
|SMTP_EMAIL_ADDRESS       | The email address InventoryHero should send emails with       |
|SMTP_SERVER              | The smtp server used to send emails                           |
|SMTP_USERNAME            | The smtp server username to login to                          |
|SMTP_PASSWORD            | The smtp server password to login with                        |
|SMTP_PORT                | The smtp port (currently onyl 465 ssl supported)              |

### Database

<b>WIP<b>

## Credits
Thanks to: 
* My Mobile Application course colleagues and co-creator of InventoryHero: 
    * Sebastian
    * Christian 
    * Hans-Jürgen

* Other OpenSource Projects where I could turn to for implementation (as well as design) guidance:
    * [Fluidd Core](https://github.com/fluidd-core/fluidd)
    * [Spoolman](https://github.com/Donkie/Spoolman)
    * [Vikunja](https://github.com/go-vikunja/vikunja)

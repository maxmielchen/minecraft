# Minecraft
Containerized Minecraft server

## Basic usage


First you have to create a docker compose file with the name "docker-compose.yml" in your folder where you want to create your minecraft server.
and write in the following:

```yaml
version: '3.9'

services:
  minecraft_server:
    container_name: minecraft_server
    image: ghcr.io/maxmielchen/minecraft:vanilla-1.19.4-amazoncorretto-17-latest
    ports:
      - "25565:25565"
    volumes:
      - "./data:/data"
```
The first time you start the container with "docker compose up" you will see the console log and you will get the warning that the eula.txt has not yet been confirmed. What you can then do with the "sed" command.

```Bash
# Start container
docker compose up

# Accept eula
sed -i 's/eula=false/eula=true/g' data/eula.txt

# Restart container
docker compose up -d
```

Now the minecraft server should be running and you should be able to access the minecraft server using your server's hostname

## Choose Image

Each image consists of 3 parts:
- **Java runtime** (corretto-17, openjdk-8, ...)
- **Minecraft server** (vanilla, bukkit, spigot, paper, folio) 
- **Minecraft version** (1.19.4, 1.18.2, ...)


The image tags have 2 main parts and 6 properties:

- **Name**: ghcr.io/maxmielchen/minecraft
  - **Registry**: ghcr.io
  - **Owner**: maxmielchen
  - **Repository**: minecraft
  
- **Version**: vanilla-1.19.4-amazoncorretto-17-latest
  - **Server**: vanilla-1.19
  - **Java runtime**: amazoncorretto-17
  - **Release**: latest

First you should choose which server you want:

- [vanilla](docs/vanilla.md)
- [bukkit](docs/paper.md)
- [spigot](docs/spigot.md)
- [paper](docs/paper.md)

Then you can look in the table whether your server version exists in combination with the runtime and whether it works.

## Agree EULA

The eula is in the data folder of your container: /data
You can also find other files there, such as the plugins folder and worlds.
 
> :warning: The server runtime cannot be found in this folder and is also discouraged from exchanging it
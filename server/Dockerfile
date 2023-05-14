ARG image
FROM ${image}
LABEL org.opencontainers.image.description 'Minecraft Server'
LABEL org.opencontainers.image.authors 'Max Mielchen (max@mielchen.email)'
ENV XMS=2G
ENV XMX=2G
WORKDIR /data
VOLUME [ "/data" ]
EXPOSE 25565/tcp
CMD java -Xms$XMS -Xmx$XMX -jar /server.jar --nogui --port 25565
ARG http_source
ADD $http_source /server.jar

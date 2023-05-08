ARG image
FROM ${image}
ARG http_source
ENV XMS=2G
ENV XMX=2G
ADD $http_source /server.jar
COPY eula.txt /data/
WORKDIR /data
VOLUME [ "/data" ]
EXPOSE 25565/tcp
CMD java -Xms$XMS -Xmx$XMX -jar /server.jar --nogui --port 25565

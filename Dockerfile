ARG image
ARG http_source
ARG artifact

FROM ${image}
ENV XMS=2G
ENV XMX=2G
COPY --from=source /server.jar /
ADD $http_source /server.jar
COPY eula.txt /data/
WORKDIR /data
VOLUME [ "/data" ]
EXPOSE 25565/tcp
CMD java -Xms$XMS -Xmx$XMX -jar /server.jar --nogui --port 25565

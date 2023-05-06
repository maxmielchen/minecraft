ARG http_source
ARG artifact
ARG image

FROM ubuntu:latest AS source
ENV http_source=${http_source}
ENV artifact=${artifact}
RUN apt update && apt install wget -y
RUN wget $http_source && mv $artifact server.jar

FROM ${image}
ENV XMS=2G
ENV XMX=2G
COPY --from=source /server.jar /
COPY eula.txt /data/
WORKDIR /data
VOLUME [ "/data" ]
EXPOSE 25565/tcp
CMD java -Xms$XMS -Xmx$XMX -jar /server.jar --nogui --port 25565

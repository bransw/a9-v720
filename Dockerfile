FROM ubuntu:22.04

RUN apt-get -y update && apt-get -y upgrade;

RUN apt-get -y install git python3 pip libgl1-mesa-glx mosquitto libgl1-mesa-glx libglib2.0-dev apt-utils
RUN pip install tqdm xmltodict Pillow opencv-python numpy netifaces ;


RUN mkdir /run/mosquitto; chmod 777 /run/mosquitto; chmod 777 /var/run/mosquitto;

RUN apt-get -y install nano net-tools

RUN cd; mkdir src; cd src; git clone https://github.com/bransw/a9-v720.git; cd a9-v720

EXPOSE 80
EXPOSE 6123
EXPOSE 6123/udp
EXPOSE 1883
EXPOSE 53
EXPOSE 10000-65000/udp

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

#CMD ["/bin/bash","/usr/local/bin/entrypoint.sh"]
CMD ["/bin/bash"]


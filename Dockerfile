FROM python:2.7
ENV FFMPEG_VERSION 4.1.1

RUN pip install autosub

WORKDIR /tmp
RUN curl https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o ffmpeg-release-amd64-static.tar.xz
RUN tar -xf ffmpeg-release-amd64-static.tar.xz
RUN cp ffmpeg-${FFMPEG_VERSION}-amd64-static/ffmpeg /usr/bin/ffmpeg 
RUN rm -rf ffmpeg-${FFMPEG_VERSION}-amd64-static*

ENTRYPOINT ["autosub"]

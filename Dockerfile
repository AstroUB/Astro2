# base image
FROM python:3.9-slim

# to look cool
ENV DEBIAN_FRONTEND=noninteractive

# base directory
RUN mkdir app
WORKDIR /app/

# upstream
RUN apt update && apt upgrade -y

# apt dependencies
RUN apt install --no-install-recommends -y \
    git bash ffmpeg mediainfo gcc wget \
    python3-dev procps neofetch make curl \
    libel1

# update pip and install requirements
COPY . .
RUN pip3 install -U pip \
    && pip3 install --no-cache-dir -r requirements.txt

# cleanup, if needed
RUN apt autoremove --purge
# Copy main path
COPY /app/startup

# initialise app
CMD [ "python3", "-m", "startup" ]

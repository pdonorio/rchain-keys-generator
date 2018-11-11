
ARG image_tag
FROM rchain/rnode:${image_tag}

RUN apt update && apt install -y python3-pip
# or https://unix.stackexchange.com/a/340482

COPY bash.rc /root/.bashrc

ENTRYPOINT ["/bin/sleep"]
CMD ["infinity"]

FROM mcr.microsoft.com/devcontainers/python:1.2.1-3.13-bookworm


RUN \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  apt-get update && apt-get install -y \
  usbutils \
  libimobiledevice-utils
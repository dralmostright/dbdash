FROM postgres:17

# Install OS packages for extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
      postgresql-server-dev-17 \
      postgresql-17-cron \
      postgresql-17-partman \
      postgresql-contrib \
    && rm -rf /var/lib/apt/lists/*
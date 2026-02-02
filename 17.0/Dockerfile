# Use official Odoo image as base
FROM odoo:17.0

# Set maintainer label
LABEL maintainer="nyamatoelton@gmail.com"
LABEL version="1.0"
LABEL description="Custom Odoo 17 modules with additional dependencies"

# Switch to root for package installation
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*



RUN chmod +x /entrypoint.sh

# Set working directory
WORKDIR /home/nyamato/odoo-dev/17.0

# Expose Odoo port
EXPOSE 8069 8072

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]

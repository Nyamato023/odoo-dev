#!/bin/bash
set -e

# Function to wait for database
wait_for_db() {
    echo "Waiting for database to be ready..."
    until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
        echo "Database is unavailable - sleeping"
        sleep 2
    done
    echo "Database is ready!"
}

# Wait for database if DB_HOST is set
if [ -n "$DB_HOST" ]; then
    wait_for_db
fi

# Create Odoo configuration from environment variables
if [ ! -f /etc/odoo/odoo.conf ]; then
    echo "Creating Odoo configuration..."
    envsubst < /etc/odoo/odoo.conf.template > /etc/odoo/odoo.conf
fi

# Create log directory
mkdir -p /var/log/odoo

# Set permissions
chown -R odoo:odoo /var/lib/odoo
chown -R odoo:odoo /var/log/odoo

# Execute the CMD
exec "$@"

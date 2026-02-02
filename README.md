# Odoo Development Environment Repository

## Overview
This repository provides a streamlined setup for working with multiple Odoo versions (Community + Enterprise editions) in a single development environment. It's designed to make Odoo version management and development accessible for teams and individual developers.

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git
- Node.js 16+ (for Odoo 17+)

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd odoo-dev

# Choose your Odoo version
cd odoo-17  # or odoo-18, odoo-19

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database
# Edit the corresponding .conf file (17.conf, 18.conf, or 19.conf)
# Update database credentials and paths

# Run Odoo
python odoo-bin -c ../17.conf  # or 18.conf, 19.conf
```

## Repository Structure

```
odoo-dev/
├── .gitignore              # Git ignore rules for Odoo development
├── odoo-17/                # Odoo 17 Community Edition
├── odoo-18/                # Odoo 18 Community Edition
├── odoo-19/                # Odoo 19 Community Edition
├── enterprise-17.0/        # Odoo 17 Enterprise Edition (partner access required)
├── enterprise-18.0/        # Odoo 18 Enterprise Edition (partner access required)
├── enterprise-19.0/        # Odoo 19 Enterprise Edition (partner access required)
├── 17.conf                 # Configuration for Odoo 17
├── 18.conf                 # Configuration for Odoo 18
└── 19.conf                 # Configuration for Odoo 19
```

## Configuration Files

Each version has its own configuration file:
- **17.conf**: Odoo 17 configuration
- **18.conf**: Odoo 18 configuration
- **19.conf**: Odoo 19 configuration

### Key Configuration Parameters
```ini
[options]
admin_passwd = admin12345               # Master password
addons_path = path/to/addons            # Addons directories
http_port = 8069                        # Web interface port
db_host = localhost                     # Database host
db_port = 5432                          # Database port
db_user = odoo                          # Database user
db_password = odoo                      # Database password
```

## Features

- **Multi-version Support**: Work with Odoo 17, 18, and 19 simultaneously
- **Enterprise Ready**: Includes Enterprise edition setup (requires partner access)
- **Isolated Environments**: Separate configurations prevent version conflicts
- **Easy Switching**: Quickly switch between Odoo versions
- **Version Control**: All Odoo versions under Git control

## Development Workflow

### Starting a Specific Version
```bash
# For Odoo 17
cd odoo-17
source .venv/bin/activate
python odoo-bin -c ../17.conf

# For Odoo 18
cd odoo-18
source .venv/bin/activate
python odoo-bin -c ../18.conf

# For Odoo 19
cd odoo-19
source .venv/bin/activate
python odoo-bin -c ../19.conf
```

### Custom Module Development
1. Place custom modules in: `odoo-XX/custom/addons/`
2. Update the corresponding `.conf` file's `addons_path`
3. Restart Odoo to see your modules

### Database Management
```bash
# Create database for Odoo 17
createdb odoo17 -O odoo

# Create database for Odoo 18
createdb odoo18 -O odoo

# Create database for Odoo 19
createdb odoo19 -O odoo
```

## Enterprise Edition Access

The Enterprise editions are included but require:
1. Valid Odoo Enterprise subscription
2. Partner access credentials
3. Proper SSH key configuration for repository access

**Note**: Enterprise directories may be empty initially. Contact your Odoo partner representative for access.

## Version Information

- **Odoo 17**: Long-term support version (recommended for production)
- **Odoo 18**: Latest stable version
- **Odoo 19**: Development/upcoming version

## Git Commands

### Update Odoo Versions
```bash
# Update Odoo 17
cd odoo-17
git pull origin 17.0

# Update Odoo 18
cd odoo-18
git pull origin 18.0

# Update Odoo 19
cd odoo-19
git pull origin 19.0
```

### Branch Management
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Switch between versions
git checkout 17.0
git checkout 18.0
git checkout 19.0
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify PostgreSQL is running: `sudo systemctl status postgresql`
   - Check database credentials in .conf files
   - Ensure user has proper permissions

2. **Module Not Found Errors**
   - Verify addons_path in configuration file
   - Check directory permissions
   - Ensure modules are in correct addons directory

3. **Port Already in Use**
   - Change http_port in configuration file
   - Kill existing process: `sudo lsof -ti:8069 | xargs kill -9`

### Dependency Issues
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version
```

## Maintenance

### Backup Configuration
```bash
# Backup all configurations
cp *.conf *.conf.backup

# Restore configurations
cp *.conf.backup *.conf
```

### Clean Environment
```bash
# Remove Python cache files
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# Remove log files
find . -name "*.log" -delete
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This repository contains Odoo Community Edition which is licensed under LGPLv3. Odoo Enterprise Edition requires a commercial license from Odoo S.A.

## Support

For issues related to:
- Odoo functionality: Refer to [Odoo Official Documentation](https://www.odoo.com/documentation)
- Repository setup: Check the troubleshooting section
- Enterprise access: Contact your Odoo partner

## Changelog

### Recent Updates
- Added Odoo 19 support
- Updated configuration files for all versions
- Improved directory structure for better version isolation
- Added comprehensive .gitignore for Odoo development

---

**Note**: Always test configuration changes in a development environment before applying to production systems.

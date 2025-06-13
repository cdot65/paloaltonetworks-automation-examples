# PAN-OS Admin Password Rotation Tool

A Python-based automation tool for rotating administrator passwords on Palo Alto Networks (PAN-OS) firewalls using the pan-os-python SDK.

## Features

- Automated password rotation for PAN-OS administrators
- Cryptographically secure password generation
- Environment-based configuration for security
- Comprehensive error handling and rollback capabilities
- Detailed logging for audit trails
- Dry-run mode for testing
- Password verification after rotation

## Requirements

- Python 3.8 or higher
- PAN-OS firewall (version 8.0+)
- Administrator access to the firewall
- Network connectivity to the firewall management interface

## Installation

1. Download `rotate_admin_password.py`, `requirements.txt`, and `.env.example` from the SCM download page and place them in a directory of your choice.

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
cp .env.example .env
```

5. Edit `.env` with your firewall details:

```
PANOS_HOSTNAME=your-firewall.example.com
PANOS_USERNAME=admin
PANOS_PASSWORD=current-password
```

## Usage

### Basic Usage

Rotate the password for the default admin user:

```bash
python rotate_admin_password.py
```

### Command Line Options

```bash
python rotate_admin_password.py [OPTIONS]

Options:
  --new-password PASSWORD   Provide your own new password (≥12 chars). If omitted,
                             the script generates a secure random one and asks for
                             confirmation.
  --debug                   Output full stack traces on error.
  --help                    Show help message
```

### Examples

1. Rotate password with an auto-generated password (interactive):

```bash
python rotate_admin_password.py
```

2. Rotate password with a specific value:

```bash
python rotate_admin_password.py --new-password "MyStrongPass123!"
```

3. Show full stack traces on error:

```bash
python rotate_admin_password.py --debug
```

## Configuration

### Environment Variables

| Variable         | Description                     | Required |
| ---------------- | ------------------------------- | -------- |
| `PANOS_HOSTNAME` | Firewall hostname or IP address | Yes      |
| `PANOS_USERNAME` | Administrator username          | Yes      |
| `PANOS_PASSWORD` | Current administrator password  | Yes      |

### Password Complexity

By default, generated passwords include:

- Uppercase letters (A-Z)
- Lowercase letters (a-z)
- Digits (0-9)
- Special symbols (!@#$%^&\*()\_+-=[]{}|;:,.<>?)

## Security Considerations

1. **Environment Variables**: Store credentials in `.env` file, never commit to version control
2. **File Permissions**: Ensure `.env` has restricted permissions (e.g., `chmod 600 .env`)
3. **Password Storage**: Generated passwords are displayed once - store them securely
4. **Audit Logging**: All password rotations are logged with timestamps
5. **Network Security**: Use secure network connections to the firewall

## Troubleshooting

### Common Issues

1. **Connection Failed**

   - Verify firewall hostname/IP is correct
   - Check network connectivity
   - Ensure management interface is accessible
   - Verify firewall certificates if using HTTPS

2. **Authentication Failed**

   - Confirm current credentials are correct
   - Check if account is locked
   - Verify API access is enabled for the user

3. **Password Change Failed**
   - Ensure administrator has permission to change passwords
   - Check password complexity requirements on firewall
   - Verify no pending configuration changes

### Debug Mode

Enable verbose logging for detailed troubleshooting:

```bash
python rotate_admin_password.py --debug
```

Check the console output for detailed error messages and stack traces.

## Development

### Project Structure

```
.
├── rotate_admin_password.py  # Single-file entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment configuration
└── README.md               # This file
```

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=.
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on the project repository.

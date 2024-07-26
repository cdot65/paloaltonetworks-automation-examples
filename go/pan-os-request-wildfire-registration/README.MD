# WildFire Registration Script

This Go script automates the process of registering WildFire on Palo Alto Networks firewalls managed by Panorama.

## Features

- Connects to Panorama to retrieve a list of connected devices
- Filters devices based on hostname patterns
- Concurrently registers WildFire on multiple firewalls
- Customizable concurrency level
- Verbose logging option for debugging

## Prerequisites

- Go 1.16 or higher
- Access to a Panorama instance
- Firewall credentials

## Installation

1. Clone this repository:

    ```
    git clone https://github.com/yourusername/wildfire-registration-script.git
    cd wildfire-registration-script
    ```

2. Install the required dependencies:

    ```
    go mod tidy
    ```

## Configuration

1. Create a `panorama.yaml` file with your Panorama configuration:

    ```yaml
    panorama:
      - hostname: your-panorama-hostname
    ```

2. Create a `.secrets.yaml` file with your authentication details:

    ```yaml
    auth:
      panorama:
        username: your-panorama-username
        password: your-panorama-password
      firewall:
        username: your-firewall-username
        password: your-firewall-password
    ```

## Usage

Run the script with the following command:

```
go run main.go [flags]
```

Available flags:

- `-debug int`: Debug level: 0=INFO, 1=DEBUG (default 0)
- `-concurrency int`: Number of concurrent operations (default: number of CPUs)
- `-config string`: Path to the Panorama configuration file (default "panorama.yaml")
- `-secrets string`: Path to the secrets file (default ".secrets.yaml")
- `-filter string`: Comma-separated list of hostname patterns to filter devices
- `-verbose`: Enable verbose logging

Example:

```
go run main.go -verbose -filter="fw1,fw2" -concurrency=5
```

## Output

The script will display:

1. A list of all devices retrieved from Panorama
2. WildFire registration results for each device
3. A summary of successful and failed registrations

## Error Handling

- The script will log errors for failed connections or registrations
- A timeout is set for each device registration to prevent indefinite hanging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
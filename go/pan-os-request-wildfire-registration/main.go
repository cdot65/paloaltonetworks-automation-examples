package main

import (
	"encoding/xml"
	"flag"
	"fmt"
	"log"
	"os"
	"runtime"
	"strings"
	"sync"
	"time"

	"github.com/PaloAltoNetworks/pango"
	"github.com/scrapli/scrapligo/driver/generic"
	"github.com/scrapli/scrapligo/driver/options"
	"github.com/scrapli/scrapligo/transport"
	"gopkg.in/yaml.v2"
)

// Panorama represents the configuration details for Panorama.
type Panorama struct {
	Hostname string `yaml:"hostname"`
}

// Config represents the overall configuration containing Panorama details.
type Config struct {
	Panorama []Panorama `yaml:"panorama"`
}

// AuthConfig represents the authentication configuration.
type AuthConfig struct {
	Auth struct {
		Panorama struct {
			Username string `yaml:"username"`
			Password string `yaml:"password"`
		} `yaml:"panorama"`
		Firewall struct {
			Username string `yaml:"username"`
			Password string `yaml:"password"`
		} `yaml:"firewall"`
	} `yaml:"auth"`
}

// DeviceEntry represents a single device entry from the Panorama response.
type DeviceEntry struct {
	Name            string `xml:"name,attr"`
	Serial          string `xml:"serial"`
	Hostname        string `xml:"hostname"`
	IPAddress       string `xml:"ip-address"`
	IPv6Address     string `xml:"ipv6-address"`
	Model           string `xml:"model"`
	SWVersion       string `xml:"sw-version"`
	AppVersion      string `xml:"app-version"`
	AVVersion       string `xml:"av-version"`
	WildfireVersion string `xml:"wildfire-version"`
	ThreatVersion   string `xml:"threat-version"`
}

// DevicesResponse represents the structure of the XML response from Panorama.
type DevicesResponse struct {
	XMLName xml.Name `xml:"response"`
	Status  string   `xml:"status,attr"`
	Result  struct {
		Devices struct {
			Entries []DeviceEntry `xml:"entry"`
		} `xml:"devices"`
	} `xml:"result"`
}

// Logger is a custom logger with debug levels.
type Logger struct {
	debugLevel int
	*log.Logger
}

func (l *Logger) Debug(v ...interface{}) {
	if l.debugLevel >= 1 {
		l.Printf("[DEBUG] %v", fmt.Sprintln(v...))
	}
}

func (l *Logger) Info(v ...interface{}) {
	if l.debugLevel >= 0 {
		l.Printf("[INFO] %v", fmt.Sprintln(v...))
	}
}

func main() {
	// Define command-line flags
	debugLevel := flag.Int("debug", 0, "Debug level: 0=INFO, 1=DEBUG")
	concurrency := flag.Int("concurrency", runtime.NumCPU(), "Number of concurrent operations")
	configFile := flag.String("config", "panorama.yaml", "Path to the Panorama configuration file")
	secretsFile := flag.String("secrets", ".secrets.yaml", "Path to the secrets file")
	hostnameFilter := flag.String("filter", "", "Comma-separated list of hostname patterns to filter devices")
	verbose := flag.Bool("verbose", false, "Enable verbose logging")

	// Initialize custom logger
	logger := &Logger{
		debugLevel: *debugLevel,
		Logger:     log.New(os.Stdout, "", log.Ldate|log.Ltime),
	}

	// If verbose flag is set, set debug level to 1
	if *verbose {
		logger.debugLevel = 1
	}
	flag.Parse()

	// Parse hostname filters
	filters := parseHostnameFilters(*hostnameFilter)

	// Read and parse the Panorama configuration file
	var config Config
	if err := readYAMLFile(*configFile, &config); err != nil {
		logger.Fatalf("Failed to read Panorama config: %v", err)
	}

	// Read and parse the secrets file
	var authConfig AuthConfig
	if err := readYAMLFile(*secretsFile, &authConfig); err != nil {
		logger.Fatalf("Failed to read secrets: %v", err)
	}

	if len(config.Panorama) == 0 {
		logger.Fatalf("No Panorama configuration found in the YAML file")
	}

	// Use the first Panorama configuration
	pano := config.Panorama[0]

	// Initialize the Panorama client
	client := &pango.Panorama{
		Client: pango.Client{
			Hostname: pano.Hostname,
			Username: authConfig.Auth.Panorama.Username,
			Password: authConfig.Auth.Panorama.Password,
			Logging:  pango.LogAction | pango.LogOp,
		},
	}

	logger.Info("Initializing client for", pano.Hostname)
	if err := client.Initialize(); err != nil {
		logger.Fatalf("Failed to initialize client: %v", err)
	}
	logger.Info("Client initialized for", pano.Hostname)

	// Get the list of connected devices
	allDevices, err := getConnectedDevices(client, logger)
	if err != nil {
		logger.Fatalf("Failed to get connected devices: %v", err)
	}

	// Filter devices based on hostname patterns
	deviceList := filterDevices(allDevices, filters, logger)

	logger.Info("Starting WildFire registration for", len(deviceList), "devices")

	// Create a channel to receive results
	results := make(chan string, len(deviceList))

	// Create a semaphore to limit concurrency
	sem := make(chan struct{}, *concurrency)

	logger.Info("Starting goroutines for WildFire registration")

	// Run WildFire registration command on filtered firewalls
	var wg sync.WaitGroup
	for i, device := range deviceList {
		wg.Add(1)
		go func(dev map[string]string, index int) {
			defer wg.Done()
			logger.Debug("Starting goroutine for device", index+1, ":", dev["hostname"])
			sem <- struct{}{}        // Acquire semaphore
			defer func() { <-sem }() // Release semaphore
			err := registerWildFireScrapli(dev, authConfig.Auth.Firewall.Username, authConfig.Auth.Firewall.Password, logger)
			if err != nil {
				logger.Debug("Error registering WildFire for device", index+1, ":", dev["hostname"], "-", err)
				results <- fmt.Sprintf("%s: Failed to register WildFire - %v", dev["hostname"], err)
			} else {
				logger.Debug("Successfully registered WildFire for device", index+1, ":", dev["hostname"])
				results <- fmt.Sprintf("%s: Successfully registered WildFire", dev["hostname"])
			}
		}(device, i)
	}

	// Close the results channel when all goroutines are done
	go func() {
		wg.Wait()
		close(results)
		logger.Info("All goroutines completed")
	}()

	logger.Info("Printing device list")
	// Print the device list
	fmt.Println("Device List:")
	for i, device := range deviceList {
		fmt.Printf("Device %d:\n", i+1)
		for key, value := range device {
			fmt.Printf("  %s: %s\n", key, value)
		}
		fmt.Println()
	}

	logger.Info("Waiting for WildFire registration results")
	// Collect and print WildFire registration results
	fmt.Println("WildFire Registration Results:")
	successCount := 0
	failureCount := 0
	for i := 0; i < len(deviceList); i++ {
		select {
		case result, ok := <-results:
			if !ok {
				logger.Info("Results channel closed unexpectedly")
				break
			}
			fmt.Println(result)
			if strings.Contains(result, "Successfully registered") {
				successCount++
			} else {
				failureCount++
			}
		case <-time.After(6 * time.Minute):
			logger.Info("Timeout waiting for result")
			fmt.Printf("Timeout waiting for result from device %d\n", i+1)
			failureCount++
		}
	}

	logger.Info(fmt.Sprintf("Registration complete. Successes: %d, Failures: %d", successCount, failureCount))
}

func readYAMLFile(filename string, v interface{}) error {
	data, err := os.ReadFile(filename)
	if err != nil {
		return fmt.Errorf("failed to read file: %w", err)
	}

	err = yaml.Unmarshal(data, v)
	if err != nil {
		return fmt.Errorf("failed to unmarshal YAML: %w", err)
	}

	return nil
}

func registerWildFireScrapli(device map[string]string, username, password string, logger *Logger) error {
	logger.Debug("Attempting to connect to", device["hostname"], "at", device["ip-address"])

	d, err := generic.NewDriver(
		device["ip-address"],
		options.WithAuthNoStrictKey(),
		options.WithAuthUsername(username),
		options.WithAuthPassword(password),
		options.WithTimeoutSocket(45*time.Second),
		options.WithTimeoutOps(45*time.Second),
		options.WithTransportType(transport.StandardTransport),
		options.WithSSHConfigFile(""), // This disables the use of the SSH config file
		options.WithPort(22),          // Explicitly set the port
	)
	if err != nil {
		logger.Debug("Failed to create driver:", err)
		return fmt.Errorf("failed to create driver: %v", err)
	}

	err = d.Open()
	if err != nil {
		logger.Debug("Failed to open connection:", err)
		return fmt.Errorf("failed to open connection: %v", err)
	}
	defer func(d *generic.Driver) {
		err := d.Close()
		if err != nil {

		}
	}(d)

	logger.Debug("Successfully connected to", device["hostname"])

	// Send the WildFire registration command
	cmd := "request wildfire registration channel public"
	logger.Debug("Sending WildFire registration command to", device["hostname"], "Command:", cmd)

	r, err := d.SendCommand(cmd)
	if err != nil {
		logger.Debug("Failed to send command:", err)
		return fmt.Errorf("failed to send command: %v", err)
	}
	if r.Failed != nil {
		logger.Debug("Command failed:", r.Failed)
		return fmt.Errorf("command failed: %v", r.Failed)
	}

	logger.Debug("Command output for", device["hostname"], ":", r.Result)

	// Check for the expected success message
	if !strings.Contains(r.Result, "WildFire registration for Public Cloud is triggered") {
		logger.Debug("Unexpected command output for", device["hostname"])
		return fmt.Errorf("unexpected command output: %s", r.Result)
	}

	logger.Debug("Successfully registered WildFire for", device["hostname"])
	return nil
}

func parseHostnameFilters(filterString string) []string {
	if filterString == "" {
		return nil
	}
	return strings.Split(filterString, ",")
}

func filterDevices(devices []map[string]string, filters []string, logger *Logger) []map[string]string {
	if len(filters) == 0 {
		return devices
	}

	var filteredDevices []map[string]string
	for _, device := range devices {
		hostname := device["hostname"]
		for _, filter := range filters {
			if strings.Contains(hostname, strings.TrimSpace(filter)) {
				filteredDevices = append(filteredDevices, device)
				logger.Debug("Device matched filter:", hostname)
				break
			}
		}
	}

	logger.Info("Filtered devices:", len(filteredDevices), "out of", len(devices))
	return filteredDevices
}

func getConnectedDevices(client *pango.Panorama, logger *Logger) ([]map[string]string, error) {
	cmd := "<show><devices><connected/></devices></show>"
	logger.Debug("Sending command to get connected devices")
	response, err := client.Op(cmd, "", nil, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to perform op command: %w", err)
	}
	logger.Debug("Received response for connected devices")

	var resp DevicesResponse
	if err := xml.Unmarshal(response, &resp); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %w", err)
	}

	if resp.Status != "success" {
		return nil, fmt.Errorf("operation failed: %s", resp.Status)
	}

	var deviceList []map[string]string
	logger.Debug("Number of devices found:", len(resp.Result.Devices.Entries))
	for _, entry := range resp.Result.Devices.Entries {
		device := map[string]string{
			"serial":           entry.Serial,
			"hostname":         entry.Hostname,
			"ip-address":       entry.IPAddress,
			"ipv6-address":     entry.IPv6Address,
			"model":            entry.Model,
			"sw-version":       entry.SWVersion,
			"app-version":      entry.AppVersion,
			"av-version":       entry.AVVersion,
			"wildfire-version": entry.WildfireVersion,
			"threat-version":   entry.ThreatVersion,
		}
		deviceList = append(deviceList, device)
		logger.Debug("Added device to list:", entry.Hostname)
	}

	logger.Debug("Total devices in list:", len(deviceList))
	return deviceList, nil
}

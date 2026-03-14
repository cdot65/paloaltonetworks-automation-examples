package main

import (
	"encoding/xml"
	"fmt"
	"log"
	"os"
	"sync"

	"github.com/PaloAltoNetworks/pango"
	"gopkg.in/yaml.v2"
)

// Firewall represents the configuration details for a single firewall.
type Firewall struct {
	Hostname string `yaml:"hostname"`
	Username string `yaml:"username"`
	Password string `yaml:"password"`
	APIKey   string `yaml:"api_key"` // Adding API Key for authentication
}

// Config represents the overall configuration containing a list of firewalls.
type Config struct {
	Firewalls []Firewall `yaml:"firewalls"`
}

// Response represents the structure of the XML response from the firewall.
type Response struct {
	Status string `xml:"status,attr"`
	Result string `xml:"result"`
}

func main() {
	var config Config

	// Read the YAML configuration file.
	data, err := os.ReadFile("firewalls.yaml")
	if err != nil {
		log.Fatalf("Failed to read file: %v", err)
	}

	// Unmarshal the YAML file into the config struct.
	err = yaml.Unmarshal(data, &config)
	if err != nil {
		log.Fatalf("Failed to unmarshal YAML: %v", err)
	}

	var wg sync.WaitGroup

	// Iterate over each firewall configuration and start a goroutine to handle each one.
	for _, fw := range config.Firewalls {
		wg.Add(1)
		go func(fw Firewall) {
			defer wg.Done()
			err := clearCounter(fw)
			if err != nil {
				log.Printf("Failed to clear counter on %s: %v", fw.Hostname, err)
			}
		}(fw)
	}

	// Wait for all goroutines to finish.
	wg.Wait()
}

// clearCounter initializes a client for the firewall, sends an API command to clear counters,
// and processes the response.
func clearCounter(fw Firewall) error {
	// Initialize the firewall client.
	client := &pango.Firewall{
		Client: pango.Client{
			Hostname: fw.Hostname,
			Username: fw.Username,
			Password: fw.Password,
			Logging:  pango.LogAction | pango.LogOp, // Enable logging
		},
	}

	log.Printf("Initializing client for %s", fw.Hostname)
	if err := client.Initialize(); err != nil {
		return fmt.Errorf("failed to initialize client: %w", err)
	}
	log.Printf("Client initialized for %s", fw.Hostname)

	// Define the command to clear the counters.
	cmd := "<clear><rule-hit-count><vsys><vsys-name><entry name='vsys1'><rule-base><entry name='security'><rules><all/></rules></entry></rule-base></entry></vsys-name></vsys></rule-hit-count></clear>"
	log.Printf("Sending command to %s", fw.Hostname)
	response, err := client.Op(cmd, "", nil, nil)
	if err != nil {
		return fmt.Errorf("failed to perform op command: %w", err)
	}
	log.Printf("Received response from %s", fw.Hostname)

	// Unmarshal the XML response into the Response struct.
	var resp Response
	if err := xml.Unmarshal([]byte(response), &resp); err != nil {
		return fmt.Errorf("failed to unmarshal response: %w", err)
	}

	// Check the response status.
	if resp.Status != "success" {
		return fmt.Errorf("operation failed: %s", resp.Result)
	}

	log.Printf("Successfully cleared counters on %s", fw.Hostname)
	return nil
}
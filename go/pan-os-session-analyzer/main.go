package main

import (
	"encoding/xml"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/PaloAltoNetworks/pango"
	"gopkg.in/yaml.v2"
)

// Settings represents the structure of settings.yaml
type Settings struct {
	Hostname string `yaml:"hostname"`
	Minutes  int    `yaml:"minutes"`
}

// Secrets represents the structure of .secrets.yaml
type Secrets struct {
	APIKey string `yaml:"api_key"`
}

// SessionEntry represents a single session entry in the XML response
type SessionEntry struct {
	XMLName     xml.Name `xml:"entry"`
	ID          string   `xml:"idx"`
	StartTime   string   `xml:"start-time"`
	Source      string   `xml:"source"`
	Destination string   `xml:"dst"`
	Application string   `xml:"application"`
	State       string   `xml:"state"`
}

// SessionResponse represents the entire XML response structure
type SessionResponse struct {
	XMLName xml.Name       `xml:"response"`
	Result  []SessionEntry `xml:"result>entry"`
}

func main() {
	// Initialize logger
	logger := log.New(os.Stdout, "INFO: ", log.Ldate|log.Ltime|log.Lshortfile)

	// Load settings
	settings, err := loadSettings("settings.yaml")
	if err != nil {
		logger.Fatalf("Error loading settings: %v", err)
	}

	// Load secrets
	secrets, err := loadSecrets(".secrets.yaml")
	if err != nil {
		logger.Fatalf("Error loading secrets: %v", err)
	}

	// Initialize pango client
	client := &pango.Firewall{
		Client: pango.Client{
			Hostname: settings.Hostname,
			ApiKey:   secrets.APIKey,
		},
	}

	// Initialize the client
	if err := client.Initialize(); err != nil {
		logger.Fatalf("Failed to initialize client: %v", err)
	}

	// Perform the API request
	cmd := "<show><session><all/></session></show>"
	resp, err := client.Op(cmd, "", nil, nil)
	if err != nil {
		logger.Fatalf("Error performing API request: %v", err)
	}

	// Parse the XML response
	var sessionResp SessionResponse
	if err := xml.Unmarshal(resp, &sessionResp); err != nil {
		logger.Fatalf("Error parsing XML response: %v", err)
	}

	// Process session entries
	fmt.Printf("Sessions older than %d minutes:\n", settings.Minutes)
	fmt.Println("------------------------------------")
	for _, entry := range sessionResp.Result {
		old, err := isOlderThanMinutes(entry.StartTime, settings.Minutes)
		if err != nil {
			log.Printf("Error processing session %s: %v", entry.ID, err)
			continue
		}
		if old {
			fmt.Printf("Session ID: %s\n", entry.ID)
			fmt.Printf("  Start Time: %s\n", entry.StartTime)
			fmt.Printf("  Source: %s\n", entry.Source)
			fmt.Printf("  Destination: %s\n", entry.Destination)
			fmt.Printf("  Application: %s\n", entry.Application)
			fmt.Printf("  State: %s\n", entry.State)
			fmt.Println("------------------------------------")
		}
	}
}

// loadSettings loads the settings from the YAML file
func loadSettings(filename string) (*Settings, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	var settings Settings
	err = yaml.Unmarshal(data, &settings)
	if err != nil {
		return nil, err
	}

	return &settings, nil
}

// loadSecrets loads the secrets from the YAML file
func loadSecrets(filename string) (*Secrets, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	var secrets Secrets
	err = yaml.Unmarshal(data, &secrets)
	if err != nil {
		return nil, err
	}

	return &secrets, nil
}

// isOlderThanMinutes checks if the given timestamp is older than the specified number of minutes
func isOlderThanMinutes(timestamp string, minutes int) (bool, error) {
	// Parse the timestamp
	t, err := time.Parse("Mon Jan 2 15:04:05 2006", timestamp)
	if err != nil {
		return false, fmt.Errorf("error parsing timestamp: %v", err)
	}

	// Check if the timestamp is older than the specified number of minutes
	return time.Since(t) > time.Duration(minutes)*time.Minute, nil
}

/**
 * Represents an individual firewall with properties and platform as FirewallPlatform
 */
export interface Firewall {
    api_key: string;
    hostname: string;
    ipv4_address: string;
    ipv6_address: string;
    notes: string;
    platform: FirewallPlatform;
    uuid: string;
}

/**
 * Represents a Firewall platform
 */
export interface FirewallPlatform {
    name: string;
}

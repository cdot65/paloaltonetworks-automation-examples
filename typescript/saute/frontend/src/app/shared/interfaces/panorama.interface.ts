/**
 * Represents an individual Panorama with properties and platform as PanoramaPlatform
 */
export interface Panorama {
    api_key: string;
    hostname: string;
    ipv4_address: string;
    ipv6_address: string;
    notes: string;
    platform: PanoramaPlatform;
    uuid: string;
}

/**
 * Represents a Panorama platform
 */
export interface PanoramaPlatform {
    name: string;
}

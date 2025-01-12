import os
import hashlib
import requests
import json
from typing import List, Optional
from config import settings


def calculate_sha256(file_path: str) -> str:
    """
    Calculate the SHA-256 hash of a file.

    This function reads the file specified by the `file_path` parameter in chunks of 4096 bytes
    and updates the SHA-256 hash object with each chunk. It returns the hexadecimal representation
    of the calculated hash.

    Args:
        file_path (str): The path to the file for which the SHA-256 hash needs to be calculated.

    Returns:
        str: The hexadecimal representation of the calculated SHA-256 hash.

    Raises:
        FileNotFoundError: If the specified `file_path` does not exist.
        IOError: If there is an error reading the file.

    Example:
        ```python
        file_path = "path/to/file.txt"
        sha256_hash = calculate_sha256(file_path)
        print(f"SHA-256 hash of {file_path}: {sha256_hash}")
        ```

    Mermaid Workflow:
        ```mermaid
        graph TD
            A[Start] --> B[Initialize SHA-256 hash object]
            B --> C[Open file at file_path]
            C --> D{Read chunk of 4096 bytes}
            D -->|Chunk read| E[Update SHA-256 hash object with chunk]
            E --> D
            D -->|End of file| F[Close file]
            F --> G[Get hexadecimal representation of SHA-256 hash]
            G --> H[Return hexadecimal representation]
        ```
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def get_file_hashes(directory: str) -> List[str]:
    """
    Calculate the SHA-256 hash values for all files in a given directory.

    This function iterates over all files in the specified directory and calculates
    the SHA-256 hash value for each file. It returns a list of hash values.

    Args:
        directory (str): The path to the directory containing the files.

    Returns:
        List[str]: A list of SHA-256 hash values for the files in the directory.

    Raises:
        FileNotFoundError: If the specified directory is not found.

    Mermaid Workflow:
        ```mermaid
        graph TD
            A[Start] --> B{Directory exists?}
            B -->|Yes| C[Initialize empty list for hashes]
            C --> D{Iterate over files in directory}
            D -->|File| E[Calculate SHA-256 hash of file]
            E --> F[Append hash value to list]
            F --> D
            D -->|No more files| G[Return list of hashes]
            B -->|No| H[Raise FileNotFoundError]
            H --> I[Print error message]
            I --> J[End]
        ```
    """
    hashes = []
    try:
        # Iterate over all files in the specified directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            # Check if the current item is a file (not a directory)
            if os.path.isfile(file_path):
                # Calculate the SHA-256 hash value of the file
                hash_value = calculate_sha256(file_path)
                # Append the hash value to the list of hashes
                hashes.append(hash_value)
    except FileNotFoundError as e:
        # Handle the case when the specified directory is not found
        print(f"Error: Directory '{directory}' not found. {e}")
        raise
    return hashes


def threat_vault_lookup(sha256_list: List[str]) -> Optional[dict]:
    """
    Perform a ThreatVault API lookup for the given list of SHA256 hashes.

    This function sends a POST request to the ThreatVault API endpoint with the provided
    list of SHA256 hashes. It retrieves the threat data associated with the hashes and
    returns the response as a dictionary if successful. If an error occurs during the API
    request or JSON parsing, it returns None and prints an error message.

    Args:
        sha256_list (List[str]): A list of SHA256 hashes to lookup in ThreatVault.

    Returns:
        Optional[dict]: The threat data retrieved from ThreatVault, or None if an error occurs.

    Mermaid Workflow:
        ```mermaid
        graph TD
            A[Start] --> B[Prepare API request]
            B --> C{Send POST request to ThreatVault API}
            C -->|Success| D[Parse JSON response]
            C -->|Error| E[Print error message and return None]
            D -->|Success| F[Return threat data]
            D -->|Error| G[Print error message and return None]
        ```
    """
    url = f'https://{settings.baseurl}/v1/threats'
    headers = {
        'X-API-KEY': settings.apikey,
        'Content-Type': 'application/json'
    }
    data = {
        'sha256': sha256_list
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 404:
            print(f"Error: API endpoint not found. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during API request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error occurred while parsing JSON response: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def main() -> None:
    """
    Main function to demonstrate the usage of the threat_vault_lookup function.

    This function performs the following steps:
    1. Defines the directory path where the files are located.
    2. Attempts to retrieve SHA256 hashes of the files in the specified directory using the get_file_hashes function.
       - If a FileNotFoundError occurs, it means the directory does not exist, and the function returns.
    3. Checks if any SHA256 hashes were found.
       - If no hashes are found, it prints a message indicating that no files were found in the directory and returns.
    4. Calls threat_vault_lookup function to retrieve threat data associated with the SHA256 hashes from ThreatVault.
    5. If the lookup is successful and threat data is retrieved:
       - Prints the retrieved data in a formatted JSON string using json.dumps with indentation.
    6. If the lookup fails and no threat data is retrieved:
       - Prints an error message indicating the failure to retrieve the threat data from ThreatVault.

    Note: The threat_vault_lookup function is called twice in this example, demonstrating that it can be used multiple
    times with the same set of SHA256 hashes.

    Mermaid Workflow:
    ```mermaid
    graph TD
        A[Start] --> B[Define directory path]
        B --> C{Get SHA256 hashes of files in directory}
        C -->|FileNotFoundError| D[Return]
        C --> E{Check if any SHA256 hashes were found}
        E -->|No| F[Print message: No files found in directory]
        F --> D
        E -->|Yes| G[Call threat_vault_lookup with SHA256 hashes]
        G --> H{Check if threat data is retrieved}
        H -->|Yes| I[Print retrieved data as formatted JSON]
        H -->|No| J[Print error message: Failed to retrieve threat data]
        I --> K[Call threat_vault_lookup again with the same SHA256 hashes]
        K --> L{Check if threat data is retrieved}
        L -->|Yes| M[Print retrieved data as formatted JSON]
        L -->|No| N[Print error message: Failed to retrieve threat data]
        M --> O[End]
        N --> O
    ```
    """
    directory = "files"
    try:
        sha256_list = get_file_hashes(directory)
    except FileNotFoundError:
        # Directory does not exist, return from the function
        return

    if not sha256_list:
        print(f"No files found in the '{directory}' directory.")
        return

    # Call threat_vault_lookup with the obtained SHA256 hashes
    result = threat_vault_lookup(sha256_list)
    if result:
        # Threat data retrieved successfully, print it as formatted JSON
        print(json.dumps(result, indent=2))
    else:
        # Failed to retrieve threat data from ThreatVault
        print("Failed to retrieve threat data from ThreatVault.")

    # Call threat_vault_lookup again with the same SHA256 hashes
    result = threat_vault_lookup(sha256_list)
    if result:
        # Threat data retrieved successfully, print it as formatted JSON
        print(json.dumps(result, indent=2))
    else:
        # Failed to retrieve threat data from ThreatVault
        print("Failed to retrieve threat data from ThreatVault.")


if __name__ == '__main__':
    main()

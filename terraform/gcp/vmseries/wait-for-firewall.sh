#!/bin/bash

# Script to wait for Palo Alto Networks firewall to become ready
# Usage: ./wait-for-firewall.sh [IP_ADDRESS] [MAX_ATTEMPTS]

FIREWALL_IP="${1:-34.45.90.210}"
MAX_ATTEMPTS="${2:-60}"
SLEEP_INTERVAL=10

echo "Waiting for firewall at https://${FIREWALL_IP} to become ready..."
echo "Max attempts: ${MAX_ATTEMPTS}, checking every ${SLEEP_INTERVAL} seconds"
echo ""

attempt=1
while [ $attempt -le $MAX_ATTEMPTS ]; do
    echo "[Attempt $attempt/$MAX_ATTEMPTS] Checking firewall status..."
    
    # Use curl with:
    # -k: allow insecure SSL (self-signed certs)
    # -s: silent mode
    # -f: fail silently on HTTP errors
    # -o /dev/null: discard output
    # -w "%{http_code}": write out HTTP status code
    # --connect-timeout: timeout for connection
    # --max-time: maximum time allowed for transfer
    
    http_code=$(curl -k -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 10 https://${FIREWALL_IP} 2>/dev/null)
    curl_exit_code=$?
    
    # Check if curl succeeded and got any HTTP response
    # For PAN firewalls, we typically get 200, 302, or 401 when ready
    if [ $curl_exit_code -eq 0 ] && [ ! -z "$http_code" ] && [ "$http_code" != "000" ]; then
        echo "✓ Firewall is ready! (HTTP Status: $http_code)"
        echo ""
        echo "The firewall at https://${FIREWALL_IP} is now responding."
        exit 0
    else
        if [ "$http_code" = "000" ] || [ -z "$http_code" ]; then
            echo "  → No response yet (connection failed or timeout)"
        else
            echo "  → Got HTTP $http_code, waiting for valid response..."
        fi
    fi
    
    if [ $attempt -lt $MAX_ATTEMPTS ]; then
        echo "  → Waiting ${SLEEP_INTERVAL} seconds before next attempt..."
        echo ""
        sleep $SLEEP_INTERVAL
    fi
    
    ((attempt++))
done

echo ""
echo "✗ Timeout: Firewall did not become ready after $MAX_ATTEMPTS attempts."
echo "  Total time waited: $((MAX_ATTEMPTS * SLEEP_INTERVAL)) seconds"
exit 1


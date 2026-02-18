import requests
import json
import time
import sys

# ========================
# domain argument ("python3 script.py example.com") or enter when prompted
if len(sys.argv) > 1:
    TARGET_DOMAIN = sys.argv[1]
else:
    TARGET_DOMAIN = input("What domain would you like to find? ")
# ========================

def fetch_certificates(domain: str, retries: int = 5) -> list[dict]:
# fetch certifications for given domain
    url = f"https://crt.sh/json?q={domain}"

    for attempt in range(1, retries + 1):
        try:
            print(f"Attempt {attempt} of {retries}...")
            response = requests.get(url, timeout=60)

            if response.status_code == 503:
                print(f"crt.sh returned 503 on attempt {attempt}.")
                if attempt < retries:
                    wait = 10 * attempt
                    print(f"Retrying in {wait} seconds...")
                    time.sleep(wait)
                    continue
                else:
                    print("All attempts failed. crt.sh is currently unavailable, try again later.")
                    response.raise_for_status()

            response.raise_for_status()
            return response.json()

        except requests.exceptions.ReadTimeout:
            print(f"Request timed out on attempt {attempt}.")
            if attempt < retries:
                print("Retrying in 10 seconds...")
                time.sleep(10)
            else:
                print("All attempts failed due to timeout.")
                raise

def parse_certificates(certs: list[dict]) -> list[dict]:
#    parse, filter to post-2024, and "deduplicate" (just remove repeats) by common_name + year
    parsed = []
    seen = set()

    for cert in certs:
        not_before = cert.get("not_before", "")
        common_name = cert.get("common_name", "")

        # Filter: only include certs from 2025 onwards
        try:
            year = int(not_before[:4])
        except (ValueError, TypeError):
            continue

        if year <= 2024:
            continue

        # remove repeats: skip if we've already seen this common_name + year combo
        dedup_key = (common_name, year)
        if dedup_key in seen:
            continue
        seen.add(dedup_key)

        parsed.append({
            "id":            cert.get("id"),
            "logged_at":     cert.get("entry_timestamp"),
            "not_before":    not_before,
            "not_after":     cert.get("not_after"),
            "common_name":   common_name,
            "name_value":    cert.get("name_value"),
            "issuer_name":   cert.get("issuer_name"),
            "serial_number": cert.get("serial_number"),
        })

    return parsed

def main():
    print(f"Fetching certificates for: {TARGET_DOMAIN}\n")

    raw_certs = fetch_certificates(TARGET_DOMAIN)
    print(f"Found {len(raw_certs)} certificate(s) before filtering.\n")

    parsed_certs = parse_certificates(raw_certs)
    print(f"Found {len(parsed_certs)} certificate(s) after filtering and deduplication.\n")

    for cert in parsed_certs:
        print(json.dumps(cert, indent=2))
        print("-" * 50)

    with open(f"{TARGET_DOMAIN}_certs.json", "w") as f:
        json.dump(parsed_certs, f, indent=2)
    print(f"\nResults saved to {TARGET_DOMAIN}_certs.json")

if __name__ == "__main__":
    main()

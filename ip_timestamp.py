from google.cloud import compute_v1
from google.oauth2 import service_account
import json
import logging
from datetime import datetime

# Configuration
PROJECT_ID = 'steady-service-429006-t5'
FIREWALL_RULE_NAME = 'admin-allow-ssh'
SERVICE_ACCOUNT_JSON = "D:\\Job_and_project\\firewall-cleanup\\your-service-account-file.json"
IP_USAGE_FILE = 'ip_usage.json'

# Set up logging for testing
test_logfile = datetime.now().strftime('ip-usage-test-%Y_%m_%d.log')
logging.basicConfig(filename=test_logfile,
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s() - %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    level=logging.INFO)
logger = logging.getLogger('IPUsage')

def get_client():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_JSON
        )
        client = compute_v1.FirewallsClient(credentials=credentials)
        return client
    except Exception as e:
        logger.error(f"Error initializing client: {e}")
        raise

def get_firewall_rule(client):
    try:
        firewall_rule = client.get(
            project=PROJECT_ID,
            firewall=FIREWALL_RULE_NAME
        )
        return firewall_rule
    except Exception as e:
        logger.error(f"Error fetching firewall rule: {e}")
        return None

def load_ip_usage():
    try:
        with open(IP_USAGE_FILE, 'r') as f:
            ip_usage = json.load(f)
        return ip_usage
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error reading IP usage file: {e}")
        return {}

def save_ip_usage(ip_usage):
    try:
        with open(IP_USAGE_FILE, 'w') as f:
            json.dump(ip_usage, f, indent=4)
        logger.info(f"IP usage file '{IP_USAGE_FILE}' updated successfully.")
    except Exception as e:
        logger.error(f"Error saving IP usage file: {e}")

def update_ip_usage(ip_ranges):
    ip_usage = load_ip_usage()
    updated = False

    for ip in ip_ranges:
        if ip not in ip_usage:
            ip_usage[ip] = datetime.now().isoformat()
            updated = True

    if updated:
        save_ip_usage(ip_usage)

def main():
    client = get_client()
    
    firewall_rule = get_firewall_rule(client)
    if not firewall_rule:
        logger.warning("No firewall rule found.")
        return
    
    current_source_ranges = firewall_rule.source_ranges
    logger.info(f"Current IP ranges: {current_source_ranges}")

    update_ip_usage(current_source_ranges)

if __name__ == '__main__':
    main()

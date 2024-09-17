from google.cloud import compute_v1
from google.api_core.exceptions import NotFound
import json
import logging
from datetime import datetime, timedelta

# Configuration
PROJECT_ID = 'steady-service-429006-t5'
FIREWALL_RULE_NAME = 'admin-allow-ssh'
IP_USAGE_FILE = 'ip_usage.json'

# Set up logging for testing
test_logfile = datetime.now().strftime('cleanup-ip-%Y_%m_%d.log')
logging.basicConfig(filename=test_logfile,
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s() - %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    level=logging.INFO)
logger = logging.getLogger('CleanupUsage')

def load_ip_usage():
    try:
        with open(IP_USAGE_FILE, 'r') as f:
            ip_usage = json.load(f)
        return ip_usage
    except FileNotFoundError:
        logger.warning(f"IP usage file '{IP_USAGE_FILE}' not found.")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error reading IP usage file: {e}")
        return {}

def filter_recent_ips(ip_usage, minutes=2):
    cutoff_time = datetime.now() - timedelta(minutes=minutes)
    filtered_ips = {
        ip: timestamp for ip, timestamp in ip_usage.items()
        if datetime.fromisoformat(timestamp) > cutoff_time
    }
    return filtered_ips

def update_firewall_rule(project_id, firewall_rule_name, ip_ranges):
    # Initialize the Compute Engine client
    firewall_client = compute_v1.FirewallsClient()
    operation_client = compute_v1.GlobalOperationsClient()

    try:
        # Retrieve the existing firewall rule
        firewall_rule = firewall_client.get(project=project_id, firewall=firewall_rule_name)

        # Current IP ranges before updating
        current_ip_ranges = set(firewall_rule.source_ranges)
        logger.info(f"Current IP ranges in firewall rule: {current_ip_ranges}")

        # New IP ranges to be applied
        new_ip_ranges = set(ip_ranges.keys())

        # Determine IPs to remove
        removed_ips = current_ip_ranges - new_ip_ranges

        if removed_ips:
            logger.info(f"Removed IP ranges: {', '.join(removed_ips)}")
        
        if not removed_ips:
            logger.info("No IP ranges were removed.")
            return  # Exit the function if no changes are needed
        
        # Update the firewall rule with the new IP ranges
        firewall_rule.source_ranges = list(new_ip_ranges)
        
        # Update the firewall rule with the new configuration
        operation = firewall_client.patch(
            project=project_id,
            firewall=firewall_rule_name,
            firewall_resource=firewall_rule
        )

        # Wait for the operation to complete
        op_name = operation.name
        logger.info(f"Operation initiated: {op_name}")
        logger.info(f"Waiting for operation {op_name} to complete...")
        operation_client.wait(project=project_id, operation=op_name)

        logger.info(f"Firewall rule '{firewall_rule_name}' updated successfully.")

    except NotFound:
        logger.error(f"Firewall rule '{firewall_rule_name}' not found in project '{project_id}'.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

def main():
    ip_usage = load_ip_usage()
    if not ip_usage:
        logger.warning("No IP usage data found.")
        return

    # Filter out IPs not used in the last 2 minutes
    recent_ips = filter_recent_ips(ip_usage)

    logger.info(f"Filtered IP ranges: {recent_ips.keys()}")

    # Update firewall rule with the filtered IPs
    update_firewall_rule(PROJECT_ID, FIREWALL_RULE_NAME, recent_ips)

if __name__ == '__main__':
    main()

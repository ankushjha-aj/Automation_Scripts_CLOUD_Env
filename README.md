## FIREWALL CLEANUP
This repository contains two Python scripts designed to manage and clean up firewall rules in Google Cloud Platform (GCP):

- ip-usage.py: Monitors and logs the IP addresses that access your firewall. It generates a JSON file (ip_usage.json) containing the IP addresses and their last access timestamps.

- cleanup-ip.py:  Analyzes the ip_usage.json file and updates  your firewall rule to only allow recently active IP addresses. This helps to improve security by removing stale or unused access rules.

## Prerequisites
Before running these scripts, ensure you have the following:
- Google Cloud SDK installed on your machine.
- A Google Cloud project with a firewall rule set up.
- A service account with the necessary permissions to manage firewall rules.
- The Google Cloud SDK authenticated with your service account credentials.
- Python 3.7 or later installed on your machine.
- The `google-cloud-firewall` and `google-cloud-storage` libraries installed using pip: `
- pip install google-cloud-firewall google-cloud-storage`
- pip install google-cloud-compute google-auth

## Usage
1. Run `ip-usage.py` to generate the ip_usage.json file.
2. Run `cleanup-ip.py` to update your firewall rule based on the ip_usage.json file
3. You can adjust the `--days` flag in `cleanup-ip.py` to specify the number of days to keep the IP addresses in the firewall rule.
4. You can also adjust the `--threshold` flag in `cleanup-ip.py` to specify the minimum number of times an IP address must have accessed your firewall in the specified time period to be
included in the updated rule.

## Limitations
- These scripts assume you have a single firewall rule set up in your GCP project. If you have multiple rules, you may need to modify the scripts to accommodate this.
- The `ip-usage.py` script logs all IP addresses that access your firewall, which may generate a large amount of data. You may want to consider filtering or sampling the data to reduce the volume.
- The `cleanup-ip.py` script removes IP addresses from the firewall rule that have not accessed your firewall in the specified time period. This may result in some legitimate users being blocked if they have not accessed your firewall recently.

## Contributing
If you have any suggestions or improvements, please feel free to submit a pull request or open an issue.

## Disclaimer
These scripts are provided as-is, without any warranty or support. Use them at your own risk.
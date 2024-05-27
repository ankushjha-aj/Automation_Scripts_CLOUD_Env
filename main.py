from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import compute_v1

# Replace with your project ID
PROJECT_ID = 'caramel-binder-418406'

# Replace with your network target tag
NETWORK_TARGET_TAG = 'ssh-allow-automation-script'

# Replace with your instance names
INSTANCE_NAMES = ['gcp-tests']

# Create the Compute Engine client
compute = build('compute', 'v1')

# Create the firewall rule
# Replace with your project ID
PROJECT_ID = 'caramel-binder-418406'

# Replace with your network target tag
NETWORK_TARGET_TAG = 'ssh-allow-automation-script'

# Create the Compute Engine client
compute = build('compute', 'v1')

# Define the firewall rule
firewall_rule = {
    'name': 'allow-ssh-access-automation',
    'network': f'projects/{PROJECT_ID}/global/networks/default',
    'targetTags': [NETWORK_TARGET_TAG],
    'allowed': [
        {
            'IPProtocol': 'all'
        }
    ]
}

# Check if the firewall rule already exists
try:
    response = compute.firewalls().get(project=PROJECT_ID, firewall=firewall_rule['name']).execute()
    print(f'Firewall rule {firewall_rule["name"]} already exists')
except HttpError:
    # Create the firewall rule if it doesn't exist
    try:
        response = compute.firewalls().insert(project=PROJECT_ID, body=firewall_rule).execute()
        print(f'Firewall rule created: {response["name"]}')
    except HttpError as error:
        print(f'Error creating firewall rule: {error}')


# Assign the target tag to the instances
def add_network_tags_to_instance(project_id, zone, instance_id, tags):
    compute = compute_v1.InstancesClient()

    # Get the current instance configuration
    response = compute.get(project=project_id, zone=zone, instance=instance_id)
    instance = response

    # Check if the instance already has the requested tags
    if set(tags).issubset(set(response.tags.items)):
        print(f"Instance {instance_id} already has tags {tags} assigned earlier")
        return

    # Update the instance configuration with the new tags
    instance.tags = {"items": tags}

    # Update the instance
    response = compute.update(project=project_id, zone=zone, instance=instance_id, instance_resource=instance)
    print(f"Instance {instance_id} updated with tags {tags}")


# Example usage
project_id = "caramel-binder-418406"
zone = "us-west4-b"
instance_id = "3044309407034756985"
tags = ["ssh-allow-automation-script"]

add_network_tags_to_instance(project_id, zone, instance_id, tags)
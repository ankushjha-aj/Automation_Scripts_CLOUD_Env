from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import compute_v1

# Replace with your project ID
PROJECT_ID = '# your project ID'

# Replace with your network target tag
NETWORK_TARGET_TAG = '# Your network target tag name'

# Replace with your instance names
INSTANCE_NAMES = ['# Enter Your INSTANCE NAME']   

# Create the Compute Engine client
compute = build('compute', 'v1')

# Create the firewall rule
# Replace with your project ID
PROJECT_ID = '# Enter Your ProjectID' 

# Replace with your network target tag
NETWORK_TARGET_TAG = '# You can Specify Your network target tag name here' 

# Create the Compute Engine client
compute = build('compute', 'v1')

# Define the firewall rule
firewall_rule = {
    'name': '# You can define your firewall rule name here', 
    'network': f'projects/{PROJECT_ID}/global/networks/default',
    'targetTags': [NETWORK_TARGET_TAG],
    'allowed': [
        {
            'IPProtocol': 'all' # You can also change this with different protocols
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
project_id = "#Your Project ID"
zone = "# Your zone of your instance"
instance_id = "# Enter your instance id"
tags = ["# Enter your network tag name here"]

add_network_tags_to_instance(project_id, zone, instance_id, tags)

# Need CHANGES ON LINES
# LINE 6, 9, 19, 12, 22, 74, 75, 76, 77 

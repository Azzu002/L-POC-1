#creating VPC
def create_vpc(service,project,name):
    project = project
    network_body = {
        "autoCreateSubnetworks": False,
        "description": "",
        "mtu": 1460,
        "name": name,
        "routingConfig": {
            "routingMode": "GLOBAL"
    }
    }
    return service.networks().insert(project=project, body=network_body).execute()


#creating SubNet
def create_subnet(service,project,name,vpc_name,region,ip_range):
    subnetwork_body = {
        "enableFlowLogs": False,
        "ipCidrRange": ip_range,
        "name": name,
        "network": f"projects/{project}/global/networks/{vpc_name}",
        "privateIpGoogleAccess": False,
        "region": f"projects/{project}/regions/{region}",
        }
        
    return service.subnetworks().insert(project=project, region=region, body=subnetwork_body).execute()


#Creating FIREWALLS
def create_firewall(service,project,vpc_name,ip_range):
    firewall_body = {
        "kind": "compute#firewall",
        "name": "internal-allow-all-tcp-udp-icmp",
        "selfLink": f"projects/{project}/global/firewalls/internal-allow-all-tcp-udp-icmp",
        "network": f"projects/{project}/global/networks/{vpc_name}",
        "direction": "INGRESS",
        "priority": 1000,
        "allowed": [
            {"IPProtocol": "tcp","ports": ["0-65535"]},
            {"IPProtocol": "udp","ports": ["0-65535"]},
            {"IPProtocol": "icmp"}
            ],
        "sourceRanges": [ip_range,"0.0.0.0/0"]
        }
        
    return service.firewalls().insert(project=project, body=firewall_body).execute()



def create_firewall_2(service,project,vpc_name):
    firewall_body_2 = {
        "kind": "compute#firewall",
        "name": "allow-ssh-icmp",
        "selfLink": f"projects/{project}/global/firewalls/allow-ssh-icmp",
        "network": f"projects/{project}/global/networks/{vpc_name}",
        "direction": "INGRESS",
        "priority": 1000,
        "description": "allows ssh and icmp all over the net",
        "allowed": [
            {"IPProtocol": "tcp","ports": ["22"]},
            {"IPProtocol": "icmp"}],
        "sourceRanges": ["0.0.0.0/0"]
        }
    return service.firewalls().insert(project=project, body=firewall_body_2).execute()
#creating VPN-Gateways


def create_ha_vpn_gw(service,gw_name,gw_region,project,network_name):
    ha_vpn_gw_body ={
        "name": gw_name,
        "region":gw_region,
        "network": f"https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network_name}",
    }
    return service.vpnGateways().insert(project=project, region=gw_region, body=ha_vpn_gw_body).execute()


#Creating clous-Router

def create_cloud_router(service,name,asn,region,project,network_name):
    router_body = {
        "name": name,
        "asn": asn,
        "network": f"https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network_name}"
        }
    return service.routers().insert(project=project, region=region, body=router_body).execute()


#Creating VPN Tunnel

def create_vpn_tunnel_0(service,project,region,cr_name,gateway_name,name,peer_id,peer_gateway,key):
    vpnTunnel1_body = {
    "name": name,
    "vpnGateway": f"https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/vpnGateways/{gateway_name}",
    "peerGcpGateway": f"https://www.googleapis.com/compute/v1/projects/{peer_id}/regions/{region}/vpnGateways/{peer_gateway}",
    "router": f"https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/routers/{cr_name}",
    "ikeVersion": 2,
    "sharedSecret": key,
    "vpnGatewayInterface": 0
    }
    return service.vpnTunnels().insert(project=project, region=region, body=vpnTunnel1_body).execute()


def create_vpn_tunnel_1(service,project,region,cr_name,gateway_name,name,peer_id,peer_gateway,key):      
    vpnTunnel2_body = {
        "name": name,
        "ikeVersion": 2,
        "peerGcpGateway": f"https://www.googleapis.com/compute/v1/projects/{peer_id}/regions/{region}/vpnGateways/{peer_gateway}",
        "router": f"https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/routers/{cr_name}",
        "sharedSecret": key,
        "vpnGateway": f"https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/vpnGateways/{gateway_name}",
        "vpnGatewayInterface": 1
        }
    return service.vpnTunnels().insert(project=project, region=region, body=vpnTunnel2_body).execute()



#Creating INterfaces

def create_bgp_interfaces(service,network,project,Tunnel_0_name,region,name_if_0,router,if_0_ip_Range,Tunnel_1_name,name_if_1,if_1_ip_Range):
    BGP_interface_body = {
        "interfaces": [
            {
                "name": name_if_0,
                "linkedVpnTunnel":f'https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/vpnTunnels/{Tunnel_0_name}',
                "ipRange": if_0_ip_Range,
                },
            {
                "name": name_if_1,
                "linkedVpnTunnel":f'https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/vpnTunnels/{Tunnel_1_name}',
                "ipRange": if_1_ip_Range,
                }],
        "network" :f'https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}',
        'region': f'https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}',
        }
    return service.routers().patch(project=project, router=router, region=region, body=BGP_interface_body).execute()

#BGP-Connections
def create_bgp_connection_1(service,project,region,router,network,if_name_0,bgp_name_1,asn,peer_asn,ip_add_if_0,peer_ipadd_if_0,
if_name_1,ip_add_if_1,bgp_name_2,peer_ipadd_if_1):
    router_body = {
        'name': router,
        'bgp': {'advertiseMode': 'DEFAULT', 'asn': asn, 'keepaliveInterval': 20},
        "network": f"https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}",
        "bgpPeers": [
            {'advertiseMode': 'DEFAULT','bfd': {'minReceiveInterval': 1000,'minTransmitInterval': 1000,'multiplier': 5,'sessionInitializationMode': 'DISABLED'},'enable': 'TRUE','interfaceName': if_name_1,'ipAddress': ip_add_if_1,'name': bgp_name_2,'peerAsn': peer_asn,'peerIpAddress': peer_ipadd_if_1},
            {'advertiseMode': 'DEFAULT','bfd': {'minReceiveInterval': 1000,'minTransmitInterval': 1000,'multiplier': 5,'sessionInitializationMode': 'DISABLED'},'enable': 'TRUE','interfaceName': if_name_0,'ipAddress': ip_add_if_0,'name': bgp_name_1,'peerAsn': peer_asn,'peerIpAddress': peer_ipadd_if_0}
            ]
    }
    return service.routers().patch(project=project,router =router, region=region, body=router_body).execute()

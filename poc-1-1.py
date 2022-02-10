from pprint import pprint
from unicodedata import name
import time
import fun_vpn 
import fun_vm
import fun_network

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()
service = discovery.build('compute', 'v1', credentials=credentials)

#creating VPC

project_id = 'poc-1-1-339912' #input(str("Enter the Project-ID: \n")) 
vpc_name = 'test-vpc'#input(str("Enter the Name of Network: "))
fun_network.create_vpc(service,project_id,vpc_name)
print('VPC is created.....')
time.sleep(12)


#creating SubNet
subnet_name = 'test-sub'#input(str("Enter subnet name: "))
subnet_region = 'us-central1'#input(str("Enter subnet region: "))
CIDR_range = '10.0.0.0/24'#input(str("Enter CIDR range : "))
fun_network.create_subnet(service,project_id,subnet_name,vpc_name,subnet_region,CIDR_range)
print('subnet is created..')
time.sleep(10)


#Creating FIREWALLS
fun_network.create_firewall(service,project_id,vpc_name,CIDR_range)
fun_network.create_firewall_2(service,project_id,vpc_name)
time.sleep(5)


#creating vm
get_instance_name = 'test-vm'#input(str("Enter name of Instance :"))
get_zone = 'us-central1-a'#input(str("Enter zone for VM :"))
fun_vm.create_instance(service,vpc_name,subnet_name,project_id,subnet_region,get_zone,get_instance_name)
print('VM is created')

#creating VPN-Gateway and Cloud-Router
vpn_gw_name = 'test-gw'#input(str("enetre the VPN Gateway name: "))
vpn_gw_region = 'us-central1' #input(str("enter the region for VPN Gateway: "))
fun_vpn.create_ha_vpn_gw(service,vpn_gw_name,vpn_gw_region,project_id,vpc_name)


router_name = 'test-cr'#input(str("Enter router name : "))
router_asn = '65000'#input(str("enetr the router's ASN (eg: 65000 and 65001 ) : "))
fun_vpn.create_cloud_router(service,router_name,router_asn,vpn_gw_region,project_id,vpc_name)
print("gateway and cloud router  are created")
time.sleep(30)


#creating VPN-Tunnels
vpnTunnel_0_name = 'test-t0'#input(str("Enter vpn tunnel-0 name : "))
vpnTunnel_1_name = 'test-t1'#input(str("Enter vpn tunnel-1 name : "))
peer_project_id = 'poc-1-2'#input(str("Enter peer project_ID : "))
peer_gateway_name = 'peer-gw'#input(str("Enter peer gateway name : "))
shared_key = '123'#input(str("Enter shared secrete key :"))
fun_vpn.create_vpn_tunnel_0(service,project_id,vpn_gw_region,router_name,vpn_gw_name,vpnTunnel_0_name,peer_project_id,peer_gateway_name,shared_key)
fun_vpn.create_vpn_tunnel_1(service,project_id,vpn_gw_region,router_name,vpn_gw_name,vpnTunnel_1_name,peer_project_id,peer_gateway_name,shared_key)
print('Tunnel0 and Tunnel1 are created')
time.sleep(5)


#creating interface0 and interface1
interface_0_name = 'if-test-t0-to-peer-t0'#input(str("Enter Interface_0 name : "))
interface_0_ip_range = '169.254.0.1/30' #input(str("Enter the interface-0's IP-Range (eg:'169.254.0.1/30' and '169.254.0.2/30' \n"))
interface_1_name = 'if-test-t1-to-peer-t1'#input(str("Enter Interface_1 name : "))
interface_1_ip_range = '169.254.1.1/30' #input(str("Enter the interface-1's IP-Range (eg:'169.254.1.1/30' and '169.254.1.2/30' \n"))
fun_vpn.create_bgp_interfaces(service,vpc_name,project_id,vpnTunnel_0_name,vpn_gw_region,interface_0_name,router_name,interface_0_ip_range,vpnTunnel_1_name,interface_1_name,interface_1_ip_range)

time.sleep(10)

#creating BGP-connection

bgp_1_name = 'bgp-test-t0-to-peer-t0'#input(str("Enter BGP name : "))
peer_ASN = '65001'#input(str("Enter a peer router's ASN (eg-65001 and 65000) :"))
bgp_ip_add_if_0 = '169.254.0.1'#input(str("Enter the IP-add of BGP (eg: '169.254.0.1' and '169.254.0.2' ) : \n"))
peer_bgp_ip_add_if_0 = '169.254.0.2'#input(str("Enter the IP-add of peer_BGP (eg: '169.254.0.2' and '169.254.0.1') : \n"))
bgp_2_name = 'bgp-test-t1-to-peer-t1'#input(str("Enter BGP name : "))
bgp_ip_add_if_1 = '169.254.1.1'#input(str("Enter the IP-add of BGP (eg: '169.254.1.1 and '169.254.1.2') : \n"))
peer_bgp_ip_add_if_1 = '169.254.1.2'#input(str("Enter the IP-add of peer_BGP (eg: '169.254.1.2' and '169.254.1.1) : \n"))

fun_vpn.create_bgp_connection_1(service,project_id,vpn_gw_region,router_name,vpc_name,interface_0_name,bgp_1_name,router_asn,peer_ASN,bgp_ip_add_if_0,peer_bgp_ip_add_if_0,
interface_1_name,bgp_ip_add_if_1,bgp_2_name,peer_bgp_ip_add_if_1)

print(*'BGP connection established succesfully*')
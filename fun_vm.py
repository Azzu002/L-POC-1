def create_instance(service,network,subnet,project,region,zone,name):
    # Get the latest Debian Jessie image.
    image_response = service.images().getFromFamily(project='debian-cloud', family='debian-9').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone

    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': f"https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{network}",
            'subnetwork': f'https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/subnetworks/{subnet}',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

    }

    return service.instances().insert(project=project, zone=zone, body=config).execute()
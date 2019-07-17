# Control plane 
This is the Dockerfile to build odl with single node configuration. You can find the configuration in config.xml file including (mounting, adding face, adding punt, adding route). The odl.py allows the user to add face, punt, and route to the remote switch. Moreover, it allows to receive telemetry. The config file includes multiple tags (i.e., face, punt, route). Each tag allows to have the configuration of multiple remote switches. Please, follow the following steps:

* Run opendaylight 
    * /hicn/opendaylight-0.9.2/bin && ./karaf
* Install required feature   
    * feature:install odl-netconf-all odl-netconf-connector odl-restconf-all odl-netconf-topology
* run the odl.py script to push the configuration
    *  cd /hicn/cntrl/ && ./odl.py -act add
    *  ./odl.py -act [face|punt|route|telem] (Please note that -act telem is a blocking execution to receive telemetry)

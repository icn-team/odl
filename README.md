# Control plane 
This is the Docker file to build hICN VNF demo. Please follow the following instruction. You can find the configuration in config.xml file including (mounting, adding face, adding punt, adding route).

* Run opendaylight 
    * /hicn/opendaylight-0.9.2/bin && ./karaf
* Install required feature   
    * feature:install odl-netconf-all odl-netconf-connector odl-restconf-all odl-netconf-topology
* run the odl.py script to push the configuration
    *  cd /hicn/cntrl/ && ./odl.py


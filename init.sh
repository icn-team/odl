#!/bin/bash

/hicn/opendaylight-0.9.2/bin/start &
sleep 10
/hicn/opendaylight-0.9.2/bin/client feature:install \
                                    odl-netconf-all \
                                    odl-netconf-connector \
                                    odl-restconf-all \
                                    odl-netconf-topology \
				    odl-netconf-callhome-ssh

wait

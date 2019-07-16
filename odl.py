#!/usr/bin/python
import socket
import requests
import datetime
import time
import argparse
import sys
import xml.etree.ElementTree as ET

from time import sleep


# Parsing argument
parser = argparse.ArgumentParser(description='Mounting nodes to ODL')
parser.add_argument('-act', action="store",  dest='act',
                    help='Indicate your operation')
results = parser.parse_args()

SUCCESS = [200,201,202]
lip6=0
rip6=0
swif=0
ip6=0

# Mount point names
nodes = ['remote']
face_list = ['face_ids1','face_ids2','face_ids3','face_ids4','face_ids5','face_ids6']
print('Applying configuration')

def mounting():
 for node in nodes:
   response= None
   url = 'http://localhost:8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/'+str(node)
   tree = ET.parse('tnode.xml')
   root = tree.getroot()
   for elem in root:
      if(elem.tag=='{urn:TBD:params:xml:ns:yang:network-topology}node-id'):
         elem.text=str(node)
      if(elem.tag=='{urn:opendaylight:netconf-node-topology}schema-cache-directory'):
         elem.text=str(node)
      if(elem.tag=='{urn:opendaylight:netconf-node-topology}host'):
         elem.text="172.17.0.4"
   tree.write('node.xml')
   filename='node.xml'
   headers = {'content-type': 'application/xml','accept':'application/xml'}
   if str(results.act)=='del':
     response = requests.delete(url, auth=('admin', 'admin'),data=open(filename).read(),headers=headers)
   elif str(results.act)=='add':
     response = requests.put(url, auth=('admin', 'admin'),data=open(filename).read(),headers=headers)
   if response==None:
     print('usage: mount.py -del/add')
     break
   elif response.status_code in SUCCESS:
     if str(results.act)=='del':
       exit
     print(response.text)
     sleep(0.1)
   else:
     print('operation failed'+str(node)+str(response))



def facing():
  lip6=0
  rip6=0
  swif=0
  for node in nodes:
      response=None
      url=None
      tree = ET.parse('config.xml')
      root = tree.getroot()
      for faces in root:
         if faces.tag=='faces':
           for face in faces:
                 if face.tag=='lip6':
                     lip6=face.text
                 if face.tag=='rip6':
                     rip6=face.text
                 if face.tag=='swif':
                     swif=face.text
         url = 'http://localhost:8181/restconf/operations/network-topology:network-topology/topology/topology-netconf/node/'+str(node)+'/yang-ext:mount/hicn:face-ip-add'
         headers = {'content-type': 'application/xml','accept':'application/xml'}

         xtop = ET.Element('input')
         xtop.attrib["xmlns"]="urn:sysrepo:hicn"
         xroute = 'lip6'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text=str(lip6)

         xroute = 'lip4'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text='-1'

         xroute = 'rip6'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text=str(rip6)

         xroute = 'rip4'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text='-1'


         xroute = 'swif'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text=str(swif)

         final = ET.ElementTree(xtop)
         final.write('face.xml')
         filename='face.xml'
         response = requests.post(url, auth=('admin', 'admin'),data=open(filename).read(),headers=headers)
         if response.status_code in SUCCESS:
             bar.update(barcount+1)
             barcount=barcount+1
             sleep(0.1)
         else:
             print('operation failed'+str(node)+response.text)


def punting():
  ip6=0
  lent=0
  swif=0
  for node in nodes:
      response=None
      url=None
      tree = ET.parse('config.xml')
      root = tree.getroot()
      for puntes in root:
         if puntes.tag=='puntes':
          for punt in puntes:
                 if punt.tag=='ip6':
                     ip6=punt.text
                 if punt.tag=='len':
                     lent=punt.text
                 if punt.tag=='swif':
                     swif=punt.text
         url = 'http://localhost:8181/restconf/operations/network-topology:network-topology/topology/topology-netconf/node/'+str(node)+'/yang-ext:mount/hicn:punting-add'
         headers = {'content-type': 'application/xml','accept':'application/xml'}
        
         xtop = ET.Element('input')
         xtop.attrib["xmlns"]="urn:sysrepo:hicn"
         xroute = 'ip6'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text=str(ip6)

         xroute = 'ip4'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text='-1'

         xroute = 'len'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text=str(lent)

         xroute = 'swif'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text=str(swif)

         final = ET.ElementTree(xtop)
         final.write('punt.xml')
         filename='punt.xml'

         response = requests.post(url, auth=('admin', 'admin'),data=open(filename).read(),headers=headers)
         if response.status_code in SUCCESS:
               bar.update(barcount+1)
               barcount=barcount+1
               sleep(0.1)
         else:
               print('operation failed'+str(node)+response.text)



def routing():
 prefix=0
 lent=0
 faceid=0
 for node in nodes:
      response=None
      url=None
      tree = ET.parse('config.xml')
      root = tree.getroot()
      for routes in root:
         if routes.tag=='routes':
           for route in routes:
                 if route.tag=='prefix':
                     prefix=route.text
                 if route.tag=='len':
                     lent=route.text
                 if route.tag=='faceid':
                     faceid=route.text
         url = 'http://localhost:8181/restconf/operations/network-topology:network-topology/topology/topology-netconf/node/'+str(node)+'/yang-ext:mount/hicn:route-nhops-add'
         headers = {'content-type': 'application/xml','accept':'application/xml'}


         xtop = ET.Element('input')
         xtop.attrib["xmlns"]="urn:sysrepo:hicn"
         xroute = 'ip6'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text=str(prefix)

         xroute = 'ip4'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text='-1'

         xroute = 'len'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text=str(lent)


         xroute = 'face_ids0'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text=str(faceid)

         for fl in face_list:
            xroute = fl
            nnode = ET.SubElement(xtop,xroute)
            nnode.text='0'

         xroute = 'n_faces'
         nnode = ET.SubElement(xtop,xroute)
         nnode.text='1'

         final = ET.ElementTree(xtop)
         final.write('route.xml')
         filename='route.xml'


         response = requests.post(url, auth=('admin', 'admin'),data=open(filename).read(),headers=headers)
         if response.status_code in SUCCESS:
               bar.update(barcount+1)
               barcount=barcount+1
               sleep(0.1)
         else:
               print('operation failed'+str(node)+response.text)


print('Usage -act [face|punt|route|add|del]')
# Mounting node to odl
if str(results.act)!='face' and str(results.act)!='punt' and str(results.act)!='route':
 mounting()

# Adding face to the remote node
elif str(results.act)=='face':
 facing()

# Adding punt to the remote node
elif str(results.act)=='punt':
 punting()

# Adding route to the remote node
elif str(results.act)=='route':
 routing()

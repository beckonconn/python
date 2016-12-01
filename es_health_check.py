#! /usr/bin/python

# Import necessary modules. These are packaged with standard python.
import urllib2,json,array

# Open the connection
try:
  infoconn = urllib2.urlopen('http://localhost:9200/?pretty=1')
except URLError as e:
  if hasattr(e, reason):
    print "An error occurred for the following reason: ", e.reason
  elif hasattr (e, code):
    print "The server had an issue."
    print e.code

try:
  healthconn = urllib2.urlopen('http://localhost:9200/_cluster/health')
except URLError as e:
  if hasattr(e, reason):
    print "An error occurred for the following reason: ", e.reason
  elif hasattr (e, code):
    print "The server had an issue."
    print e.code

# Read data in from connection
infodata = infoconn.read()
healthdata = healthconn.read()

# Print in formatted response
print "\nElasticsearch Cluster Information \n--------------------------------"
print "Cluster Name: " + json.loads(infodata)["cluster_name"]
print "Node Name: " + json.loads(infodata)["name"]
print "Lucene Version: " + json.loads(infodata)["version"]["lucene_version"]
print "Elastic Version: " + json.loads(infodata)["version"]["number"]
print "Number of Nodes: ", json.loads(healthdata)["number_of_nodes"]
print "\nElasticsearch Cluster Health Information \n----------------------------------------"
print "Status: " + json.loads(healthdata)["status"]

# If the status field in the health data array is yellow. Create another request and search for unassigned shards
if json.loads(healthdata)["status"] == "yellow":
  try:
    yellowhunt =  urllib2.urlopen('http://localhost:9200/_cluster/state/')
  except URLError as e:
    if hasattr(e, reason):
      print "An error occurred for the following reason: ", e.reason
    elif hasattr (e, code):
      print "The server had an issue."
      print e.code

  yellowhunt_pdata = json.loads(yellowhunt.read()) 
  ypdra_length = len(yellowhunt_pdata["routing_nodes"]["unassigned"])
  unassigned_shards = []

  for count in range(ypdra_length):
    if yellowhunt_pdata["routing_nodes"]["unassigned"][count]["state"] == "UNASSIGNED":
      shard = yellowhunt_pdata["routing_nodes"]["unassigned"][count]["shard"]
      str(shard)
      unassigned_shards += [shard]
  # Print the unassigned shards and recommend a solution
  print "The following shards are unassigned: ", unassigned_shards
  print "Try the following solution to solve the issue."
  print "curl -XPUT localhost:9200/_cluster/settings -d \'{ \"transient\" : { \"cluster.routing.allocation.enable\" : \"all\" } }'"
  print "If this solution does not work, further investigation will need to be done."

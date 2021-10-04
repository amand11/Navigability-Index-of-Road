# cd ~/Desktop/Code2/MNPx
import random
from collections import Counter
from math import sin, radians, cos, asin, sqrt, ceil, floor
from lxml import etree as ET
import lxml.etree
import matplotlib.pyplot as plt


amenity_val = {'apartments': 2, 'atm': 2, 'baby_hatch': 2, 'bank': 5, 'bar': 4, 'bbq': 2, 'bicycle_rental': 2, 'biergarten': 2, 'blood_bank': 5, 'bridge': 5, 'bungalow': 2, 'bunker': 2, 'bureau_de_change': 2, 'bus_station': 7, 'cabin': 1, 'cafe': 3, 'car_rental': 3, 'cathedral': 3, 'chapel': 3, 'charging_station': 1, 'church': 3, 'cinema': 5, 'civic': 2, 'clinic': 3, 'club': 5, 'college': 5, 'commercial': 3, 'community_centre': 4, 'conservatory': 4, 'construction': 3, 'container': 2, 'cowshed': 3, 'dentist': 3, 'doctors': 4, 'drinking_water': 2, 'driving_school': 3, 'farm': 1, 'fast_food': 3, 'fire_station': 6, 'food_court': 3, 'fuel': 3, 'garage': 2, 'garages': 3, 'gatehouse': 5, 'government': 3, 'greenhouse': 4, 'grandstand': 4, 'hotel': 3, 'hospital': 7, 'house': 1, 'ice_cream': 2, 'internet_cafe': 2, 'industrial': 3, 'kindergarten': 3, 'kiosk': 1, 'language_school': 4, 'library': 2, 'monastery': 4, 'mosque': 3, 'music_school': 2, 'nightclub': 2, 'office': 2, 'parking': 2, 'pavilion': 2, 'pharmacy': 3, 'place_of_worship': 6, 'police': 7, 'post_box': 7, 'post_office': 7, 'pub': 5, 'public': 3, 'public_bath': 4, 'religious': 2, 'residential': 1, 'restaurant': 6, 'retail': 2, 'roof': 3, 'ruins': 2, 'school': 7, 'shed': 2, 'shrine': 3, 'sports_hall': 4, 'stadium': 6, 'supermarket': 3, 'taxi': 4, 'temple': 3, 'theatre': 5, 'toilets': 2, 'train_station': 6, 'transformer_tower': 3, 'transportation': 4, 'tree_house': 2, 'university': 5, 'vending_machine': 2, 'water_tower': 4, 'waste_basket': 2, 'waste_disposal': 2, 'youth_centre': 4}
highway_val = {'corridor': 2, 'footway': 1, 'living_street': 3, 'motorway':3, 'motorway_link':2, 'path': 2, 'pedestrian': 1, 'primary':3, 'primary_link':2, 'residential': 4, 'road': 6, 'secondary': 3, 'secondary_link': 2, 'service': 2, 'steps': 1, 'tertiary': 2, 'tertiary_link': 1, 'track':0.5, 'trunk': 2, 'trunk_link':2, 'unclassified': 1}




def distance(lat1, lat2, lon1, lon2): 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))*6371  
    return(c) 

def closest(data, v):
    return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))



class Node(object):
	"""docstring for Node"""
	def __init__(self, id, lon, lat, tag, visible, score=0):
		self.id = id
		self.lon = lon
		self.lat = lat
		self.tag = tag
		self.visible = visible
		self.score = score

	# def node_scoring(self):
		



class Ways(object):
	def __init__(self, id, type, tag, nd, score=0):
		self.id = id
		self.type = type
		self.tag = tag
		self.nd = nd
		self.score = score

	# def scoring(self):


		
class Relation(object):
	"""docstring for Relation"""
	def __init__(self, id, type, tag, member):
		self.arg = arg
		


def indexing(file_name):
	tree = ET.parse(file_name)
	root = tree.getroot()
	children = root.getchildren()

	node_list = []
	way_list = []
	relation_list = []
	node_score_dict = {}
	node_dict = {}
	cnt = 0
	way_node_list = []



	for c in children:
		# Gathering list of nodes in present in the Highway
		if c.tag == "way":
				typy = ""
				nd = []
				tags = []
				is_highway = False
				score = 0
				for t in c:
					if t.tag == "tag":
						typy = t.attrib["k"]
						if t.attrib["k"] == "highway":
							is_highway = True
				if is_highway:
					for t in c:
						if t.tag == "nd":
							way_node_list.append(t.attrib["ref"])




	for c in children:
		# Traverseing everynode assigning score to every node according to its amenity value
		if c.tag == "node":
			c.attrib["id"],c.attrib["lat"], c.attrib["lon"]
			tag = []
			score = 0
			for t in c:
				if t.tag == "tag":
					tag.append(t.values())
					if t.attrib["k"] == "amenity" and t.attrib["v"] in amenity_val:
						amenity_here = t.attrib["v"]
						score+=amenity_val[t.attrib["v"]]
					kl = [t.attrib["k"], t.attrib["v"]]
			
			score+=(len(tag)/5)
			node_score_dict[c.attrib["id"]] = score
			node_dict[c.attrib["id"]] = {"lon":c.attrib['lon'], "lat":c.attrib['lat'], "score":score}
			visible = True
			if "visible" in c.attrib:
				visible = c.attrib["visible"]
			node_list.append(Node(c.attrib["id"],c.attrib["lat"], c.attrib["lon"], tag, visible, score))

	for c in children:
		# If node is Building of importnce, I will find neared Highway Road node and increase that node value
		if c.tag == "node":
			score = node_score_dict[c.attrib["id"]]
			if score>3:
				min_dis = 10000
				min_j = -1
				flag = False
				for i in way_node_list:
					if i is not c.attrib["id"] and node_dict[i]["score"] < 2: 
						dis_ij = distance(float(node_dict[i]["lat"]), float(node_dict[i]["lon"]), float(c.attrib['lat']), float(c.attrib['lon'])) 
						if dis_ij<min_dis:
							min_dis = dis_ij
							min_j = i
							flag = True

				if flag==True and amenity_here in amenity_val:
					node_dict[min_j]["score"] +=amenity_val[amenity_here]
					node_score_dict[min_j] +=amenity_val[amenity_here]
				elif flag==True and min_j!=-1:	
					node_dict[min_j]["score"] +=1
					node_score_dict[min_j] +=1



	for c in children:	
		# Here it will traverse over every Building present with tag way, and usually building will have multiple nodes on its boundary
		# so if find middle point of this boudary nodes(taking avg of the given node) and find nearest nodes highway node and increae that nodes value
		if c.tag == "way":
				typy = ""
				nd = []
				tags = []
				score = 0
				amenity_here = ""
				is_building = False
				for t in c:
					if t.tag == "tag" and t.attrib["k"] == "building":
						is_building = True
					if t.tag == "tag" and t.attrib["k"] == "amenity":
						amenity_here = t.attrib["v"] 
							

				if is_building:
					node_ref_list = []
					avg_lat=0
					avg_lon=0
					for t in c:
						if t.tag == "nd":
							node_ref_list.append(t.attrib["ref"])
							avg_lon+=float(node_dict[t.attrib["ref"]]["lon"])
							avg_lat+=float(node_dict[t.attrib["ref"]]["lat"])
					
					avg_lat=avg_lat/len(node_ref_list)
					avg_lon=avg_lon/len(node_ref_list)

					min_dis = 10000
					min_j = -1
					flag = False
					for i in way_node_list:
						if i not in node_ref_list and node_dict[i]["score"]<2:
							dis_ij = distance(float(node_dict[i]["lat"]), float(node_dict[i]["lon"]), avg_lat, avg_lon) 
							if dis_ij<min_dis:
								min_dis = dis_ij
								min_j = i
								flag = True

					if flag==True and amenity_here in amenity_val:
						node_dict[min_j]["score"] +=amenity_val[amenity_here]
						node_score_dict[min_j] +=amenity_val[amenity_here]
					elif flag==True and min_j!=-1:	
						node_dict[min_j]["score"] +=1
						node_score_dict[min_j] +=1


	for c in children:
		# Here I am going through every highway road and assigning it a navigability score
		# Navigability score based on the aggreagated score of all the nodes a road has and on the type of road and number of lanes the road has
		if c.tag == "way":
				typy = ""
				nd = []
				tags = []
				score = 0
				for t in c:
					if t.tag == "tag":
						typy = t.attrib["k"]
				#Type of road and number of lane will afffect score which at end will increase the Nav_score of the Way/Road 
				#Taking Account of classifiction of road if given 
						if t.attrib["k"] == "highway" and t.attrib["v"] in highway_val:
							score+=highway_val[t.attrib["v"]]
						elif t.attrib["k"] == "highway":
							score+=1
				#Taking Account of lane information of a road if given 
						if t.attrib["k"] == "lanes":  
							score+=int(t.attrib["v"])
							

				for t in c:
					if t.tag == "nd":
						nd.append(t.attrib["ref"])
						if t.attrib["ref"] in node_score_dict:
							score+=node_score_dict[t.attrib["ref"]] 
					if t.tag == "tag":
						tags.append(t.values())

				score+=(len(tags)/5)
				if score>30:
					score = 30 	
				way_list.append(Ways(c.attrib["id"], typy, tags, nd, score))
				attrib = {'k':"nav_score", 'v':str(float(score))}
				element = c.makeelement('tag', attrib)
				c.append(element)




	


# {0: 218, 1: 2413, 2: 388, 3: 436, 4: 349, 5: 71, 6: 15, 7: 3, 8: 1, 9: 2, 10: 3, 11: 1, 12: 1, 13: 1, 14: 0, 15: 3, 16: 0}
	
	navscorelist = []
	for i in way_list:
		attrs = vars(i)
		if attrs["type"] == "highway":
			print(attrs["id"], " ",attrs["score"])
			navscorelist.append(floor(attrs["score"]))

	ma = Counter(navscorelist)
	ma = sorted(ma.items())
	map = {}
	for i in range(max(navscorelist)+1):
		map[i] = 0
	for i in ma:
		map[i[0]] = i[1]
	print(map)

	plt.bar(range(len(map)), list(map.values()), align='center')
	plt.xticks(range(len(map)), list(map.keys()))
	plt.xlabel("Navigability Score")
	plt.ylabel("Number of Roads")
	plt.show()

	tree.write('indexed.osm.xml', encoding='utf-8', pretty_print=True, xml_declaration=True)
	

indexing("map.osm.xml")
		

# {0: 0, 1: 70, 2: 112, 3: 6, 4: 92, 5: 16, 6: 22, 7: 38, 8: 18, 9: 7, 10: 22, 11: 14, 12: 19, 13: 8, 14: 9, 15: 96, 16: 0}
# {0: 520, 1: 17, 2: 6, 3: 0, 4: 1, 5: 0, 6: 0, 7: 0, 8: 1, 9: 0, 10: 3, 11: 0, 12: 0, 13: 0, 14: 1, 15: 0, 16: 0}
# {0: 0, 1: 82, 2: 143, 3: 7, 4: 123, 5: 11, 6: 18, 7: 37, 8: 29, 9: 9, 10: 20, 11: 11, 12: 13, 13: 4, 14: 10, 15: 32, 16: 0}
# {0: 0, 1: 82, 2: 143, 3: 7, 4: 123, 5: 11, 6: 18, 7: 37, 8: 29, 9: 9, 10: 20, 11: 11, 12: 13, 13: 4, 14: 10, 15: 32, 16: 0}
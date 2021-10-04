# Navigability-Index-of-Road

Brief Description:
Program takes an osm file(map.osm.xml) and returns a list of ways(k="highway") indexed with a navigability score with a graph of distribution of values. Program is deciding navigability on the basis of Type of road, number of tags and important/(Navigable) nodes it has. 
For this program gives a score to each node on the basis of its amenity value.
then looping over ways:
If a way is a building, the program scores its nearest neighbouring node(with score<2) according to amenity value(of building).
After that program counts all the score of nodes of a way with k="highway" and assigned that score to the way
at end program prints each way(k="highway") with its navigability score.

I have assigned amenity value according to me, but can be assigned in a better way based on some statistics. 

PS: PFA code. I also ran the program on parts of Delhi, results[x-axis-> Navigability Score and y-axis -> Number of ways with corresponding score] is attached

New Changes


1) Finding lane information and incorporating it. Some roads do have lane information. Currently, I am just adding a number of lanes to roads.
2)Preparing Dataset and Compressing: Now Program outputs OSM.XML(" indexed.osm.xml ") file with each way which has tag "highway" will now also have a new tag with key =  "nav_score" and value = score.

Also, I have also improved the code and Now whenever the Program encounters a Building:	
a)If Building is Single Node, I find the nearest node(that is also present on some (tagged as Highway) road) and increasing that node's score	
b)if Building is Bunch of Node, I find the central point of them(avg them out) and find the nearest node(that is also present on some (tagged as Highway) road) and increasing that node's score.
	{For this purpose program separates Nodes that are referenced in Road (tag-highway) and stores that in a list}

In the end, Program adds the score of all the nodes present on the road(tag=" highway ") and assigns that score to Road. Also, I am adding the score to the Road based on its type and number of lanes.

I have attached code, input and output file and graph for Parts of Banglore and Delhi.  I have also attached the scoring scheme when the Program encounters building with information of its amenity.
I also found that Banglore Database is much better-annotated plus contains more information.

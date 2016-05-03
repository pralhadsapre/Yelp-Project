import sys
import pymongo

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import Violation as v

def main():
    try:
        c = MongoClient('localhost', 27017)
    except ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e

    # getting a handle to the database
    db = c["projectDB"]
    print "Database connected successfully"

    worstRestaurants = []

    count = 1
    accurate = 0
    all_restaurants = db.yearlyViolationsWithTopics.find()
    for restaurant in all_restaurants:
        tempList, score, checklist = v.Violation(restaurant).makePrediction()
        worstRestaurants.append((tempList, score, checklist))
        accurate += 1 if score > 0 else 0

        sys.stdout.write("\r" + "%d restaurants processed" % count)
        sys.stdout.flush()
    	count += 1
    	
    print ""
    print "Making predictions done!"
    print "%d out of %d were correct predictions" % (accurate, count)
    print "Accuracy - %.2f" % ((accurate * 100.0) / count)

    print "Writing location data to database"
    worstRestaurants = sorted(worstRestaurants, key=lambda k: k[1], reverse = True)
    count = 1
    for x in worstRestaurants:
        # print x[0],
        # print x[1]

        if len(x[0]) >= 1:
            for yelp_ID in x[0]: 

                matchFound = False
                query = {"business_id" : { "$eq" : yelp_ID}}
                for business in db.businesses.find(query):
                    locationDict = {}
                    locationDict["latitude"] = business["latitude"]
                    locationDict["longitude"] = business["longitude"]
                    locationDict["name"] = business["name"]
                    locationDict["severity"] = x[1]
                    locationDict["business_id"] = business["business_id"]
                    locationDict["address"] = business["full_address"]
                    locationDict["checklist"] = ", ".join(x[2])

                    if "neighborhoods" in business and len(business["neighborhoods"]) > 0:
                        locationDict["locality"] = business["neighborhoods"][0]                    

                    db.violatingRestaurants.insert(locationDict)

                    sys.stdout.write("\r" + "%d restaurants written" % count)
                    sys.stdout.flush()
                    count += 1
                    matchFound = True
                
                if matchFound:
                    break

            # print worstRestaurants[x]

    print ""
    print "Check MongoDB for output data"
    c.close()

if __name__ == "__main__":
    main()     
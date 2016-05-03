import sys
import pymongo

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import RestaurantViolation as rv

def main():
    try:
        c = MongoClient('localhost', 27017)
    except ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e

    # getting a handle to the database
    db = c["projectDB"]
    print "Database connected successfully"

    groupedViolations = {}

    count = 1
    allViolations = db.violations.find()
    # print allViolations.count()

    for one_violation in allViolations:
    	if one_violation["restaurant_id"] not in groupedViolations:

    		groupedViolations[one_violation["restaurant_id"]] = rv.RestaurantViolation(one_violation)

    		# first find the mapping between violation data and yelp data
    		query = {"restaurant_id" : { "$eq" : one_violation["restaurant_id"]}}
    		for item in db.yelpID_Mapping.find(query):
    			groupedViolations[one_violation["restaurant_id"]].setYelpIDs(item)
    		
    		# second append the violation data as a JSON array
    		query = {"restaurant_id" : one_violation["restaurant_id"]}
    		for item in db.violations.find(query):
    			groupedViolations[one_violation["restaurant_id"]].addViolation(item)

    		# third when the violations are found, we proceed with sentiment analysis for each year
    		for yelp_ID in groupedViolations[one_violation["restaurant_id"]].getYelpIDs():
    			query = {"business_id" : yelp_ID}
    			for review in db.reviewsSentiment.find(query):
    				groupedViolations[one_violation["restaurant_id"]].addReview(review)

    		count += 1
    		sys.stdout.write("\r" + "%d restaurants processed" % count)
    		sys.stdout.flush()

    		db.yearlyViolationsWithTopics.insert(groupedViolations[one_violation["restaurant_id"]].getDictionary())
    		# if count == 500 or count == 1000 or count == 1500:
    		# 	print ""
    		# 	print groupedViolations[one_violation["restaurant_id"]].getDictionary()
        
    print ""
    print "Data grouping done!"

    c.close()        
        
if __name__ == "__main__":
    main()     
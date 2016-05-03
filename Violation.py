import sys

class Violation:

	max_negative = 35.0
	max_violation = 250.0
	# 55*1 + 7.0*5 + 16*10 = 250

	# Atleast one *** violation corresponds to the value of 0.2
	threshold = 0.2

	def __init__(self, restaurantDict):
		self.data = restaurantDict

	def computeViolationScore(self, violationDict):
		if "*" in violationDict:
			level1_weight = 1
			level2_weight = 5
			level3_weight = 10

			score = 5 * (level1_weight * violationDict["*"] + 
							level2_weight * violationDict["**"] + 
							level3_weight * violationDict["***"]) / Violation.max_violation
			return (score, 1)
		else:
			return (0,0)

	def computeSentimentScore(self, violationDict):
		if "stars" in violationDict and "negative" in violationDict:
			score = 2.5 * (5 - violationDict["stars"]) / 5 + 2.5 * (violationDict["negative"] / Violation.max_negative) 
			return (score, 1)
		else:
			return (0,0)

	def makePrediction(self):
		self.data["violations"] = sorted(self.data["violations"], key=lambda k: k['date'], reverse = True)

		# print self.data["violations"]

		if len(self.data["violations"]) > 1:

			validationIndex = 0
			# for i in range(len(self.data["violations"])):
			# 	if "*" in self.data["violations"][i]:
			# 		validationIndex = i
			# 		break

			# if (len(self.data["violations"]) - validationIndex) < 1:
			# 	return 0

			violationDict = self.data["violations"][validationIndex]

			violationScore = 0.0
			violationCount = 0
			sentimentScore = 0.0			
			sentimentCount = 0

			# limit = validationIndex + 3 if (len(self.data["violations"]) - validationIndex) > 3 else len(self.data["violations"])

			for x in range(validationIndex + 1, len(self.data["violations"])):
				temp, count = self.computeViolationScore(self.data["violations"][x])
				violationScore += temp
				violationCount += count

				temp, count = self.computeSentimentScore(self.data["violations"][x])
				sentimentScore += temp
				sentimentCount += count

			violationScore /= violationCount if violationCount > 0 else 1
			sentimentScore /= sentimentCount if sentimentCount > 0 else 1

			totalScore = violationScore + sentimentScore

			validationScore = 0
			temp, count = self.computeViolationScore(self.data["violations"][0])
			validationScore += temp
			temp, count = self.computeSentimentScore(self.data["violations"][0])
			validationScore += temp

			sys.stdout.write(" %.2f, %.2f" % (totalScore, validationScore))
			sys.stdout.flush()
			# print " %.2f, %.2f" % (totalScore, validationScore)
			# dummy = raw_input("")

			if totalScore > Violation.threshold and validationScore > Violation.threshold:
				return (self.data["yelp_ID"], totalScore, self.data["checklist"])
			else:
				return (self.data["yelp_ID"], 0, [])
		else:
			return (self.data["yelp_ID"], 0, [])
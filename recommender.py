import math

# Reads the movies from the movies.dat file as mov_id and mov_title
def getMovies():
	movies = {}
	with open("data/movies.dat") as input:
		for line in input:
			line = line.strip().split('::') 
			movies[int(line[0])] = line[1]
	return movies

# Reads the ratings for every user in the ratings.dat file as user_id, mov_id and mov_rating
def getRatings():
	users = {}
	with open("data/ratings.dat") as input:
		for line in input:
			line = line.strip().split('::') 
			user_id = int(line[0])
			mov_id = int(line[1])
			rating = float(line[2])
			if user_id not in users:
				users[user_id] = {}
			users[user_id][mov_id] = rating
	return users

# Gets the similarity between 2 users using pearson correlation (scaled to the number of movies)
def getUserSimilarity(user1, user2):

	number_of_similar = 0
	pearson = 0
	ratings_user1 = []
	ratings_user2 = []
	for movie in user1:
		if movie in user2:
			number_of_similar += 1
			ratings_user1.append(user1[movie])
			ratings_user2.append(user2[movie])

	if number_of_similar > 0:
		mean_user1 = sum(ratings_user1)/len(ratings_user1)
		mean_user2 = sum(ratings_user2)/len(ratings_user2)

		numerator = 0
		denominator_user1 = 0
		denominator_user2 = 0
		for i in range(number_of_similar):
			numerator += ((ratings_user1[i] - mean_user1) * (ratings_user2[i] - mean_user2))
			denominator_user1 += (ratings_user1[i] - mean_user1) * (ratings_user1[i] - mean_user1) 
			denominator_user2 += (ratings_user2[i] - mean_user2) * (ratings_user2[i] - mean_user2) 

		denominator_user1 = math.sqrt(denominator_user1)
		denominator_user2 = math.sqrt(denominator_user2)

		denominator = denominator_user1 * denominator_user2

		pearson = numerator / denominator if denominator else 0

		# Scale the result
		min_list = [float(number_of_similar)/50, 1]
		pearson *= min(min_list)

	return pearson

def getPredictions(user1, users, movies):
	neighborhoods = {}
	items_in_neighborhood = {}
	predictions = {}

	print "Calculating neighborhood of user: "+str(user1)
	neighborhoods[user1] = {}
	current_min_val = 1
	current_min_id = -1
	for user2 in users:
		if user2 != user1:
			similarity = getUserSimilarity(users[user1], users[user2])
			if len(neighborhoods[user1]) < 30:
				neighborhoods[user1][user2] = similarity
			else:
				for user_neighbor in neighborhoods[user1]:
					if neighborhoods[user1][user_neighbor] < current_min_val:
						current_min_val = neighborhoods[user1][user_neighbor]
						current_min_id = user_neighbor

				if similarity > current_min_val:
					neighborhoods[user1][user2] = similarity
					del neighborhoods[user1][current_min_id]
					current_min_id = user2
					current_min_val = similarity

	items_in_neighborhood[user1] = {}
	means = {}
	print "Finding items in neighborhood of user: "+str(user1)
	for user in neighborhoods[user1]:
		rating_mean = 0
		total = 0
		for item in users[user]:
			if item not in items_in_neighborhood[user1]:
				items_in_neighborhood[user1][item] = {}
			items_in_neighborhood[user1][item][user] = users[user][item]
			rating_mean += users[user][item]
			total += 1

		means[user] = rating_mean/total

	rating_mean = 0
	total = 0

	print "Getting average of user: "+str(user1)
	for item in users[user1]:
		rating_mean += users[user1][item]
		total += 1
	means[user1] = rating_mean/total

	print "Generating predictions for every item in the neighborhood of user: "+str(user1)
	for item in items_in_neighborhood[user1]:
		if item not in users[user1]:
			predictions[item] = means[user1]
			total = 0
			total_count = 0
			for user in items_in_neighborhood[user1][item]:
				total_count += 1
				total += neighborhoods[user1][user] * (users[user][item] - means[user])

			predictions[item] += total/total_count

	return predictions

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]

if __name__ == '__main__':

	movies = getMovies()
	users = getRatings()
	TEST_USER = 1430
	
	predictions = getPredictions(TEST_USER,users,movies)
	top_10 = []

	# Get top 10 predictions
	for i in range(20):
		item = keywithmaxval(predictions)
		top_10.append(movies[item])
		del predictions[item]

	print "Movies watched by user "+str(TEST_USER)+": "
	for mov in users[TEST_USER]:
		print movies[mov] + " "+str(users[TEST_USER][mov])
	print "Top 10: "
	print top_10

	# for user1 in users:
	# 	predictions[user1] = getPredictions(user1,users,movies)
			










	






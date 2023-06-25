import datetime
import math


#Create-ujemo graph

#TEZINE SAMIH AKICJA
comment_weight = 15

share_weight = 20

reactions_weight = {
    'hahas' : 5,
    'wows' : 6,
    'loves' : 10,
    'likes' : 4,
    'angrys' : 8,
    'sads' : 9,
    'special' : 11,
}

time_factor = 0.9   #ZA SVAKIH POLA MESECA KOJI JE PROSAO OD INTERAKCIJE RACUNA SE 0,8 OD ACTUALLY WEIGHTA

friendship_weight = 100

max_date_affinity = 60

####

##comments = parse_files.load_comments('./dataset/original_comments.csv')
##statuses = parse_files.load_statuses('./dataset/original_statuses.csv')
##reactions = parse_files.load_reactions('./dataset/original_reactions.csv')
##shares = parse_files.load_shares('./dataset/original_shares.csv')

# FACTORS
    #1) Comments or shares posts from author
    #2) Reactions on posts from author
    #3) Friendship
    #4) Time of interactions!


def define_affinity(self,other,all_users,comments,shares,reactions,statuses):

    #initial affinity
    affinity_score = 0

    #comments
    self_user = all_users[self]
    friends = self_user['friends']

    if other in friends:
        affinity_score += friendship_weight


    if self in comments.keys():
        my_comments = comments[self]
        for i in range (len(comments[self])):
            status_id = my_comments[i]['status_id']
            status = statuses[status_id]
            status_author = status['author']
            if status_author == other:
                date_time_factor = checkDateTime(my_comments[i]['comment_published'])
                affinity_score += comment_weight*date_time_factor
    if self in shares.keys():
        my_shares = shares[self]
        for i in range (len(shares[self])-1):
            status = statuses[my_shares[i]['status_id']]
            status_author = status['author']
            if status_author == other:
                date_factor = checkDateTime(my_shares[i]['status_shared'])
                affinity_score += share_weight*date_factor
    if self in reactions.keys():
        my_reactions = reactions[self]
        for i in range (len(reactions[self])):
            status = statuses[my_reactions[i]['status_id']]
            status_author = status['author']
            if status_author == other:
                type_reaction = my_reactions[i]['type_of_reaction']
                score_of_reaction = reactions_weight[type_reaction]
                date_factor = checkDateTime(my_reactions[i]['reacted'])
                affinity_score += date_factor*score_of_reaction

    return affinity_score







def checkDateTime(date):
    current_date = datetime.date.today()
    date_of_interation = date.date()
    day_difference = (current_date-date_of_interation).days
    if day_difference < 14:
        k=0.01
        result = math.exp(-k*day_difference)
    else:
        k=0.02
        result = math.exp(-k*day_difference)
    return round(result,2)





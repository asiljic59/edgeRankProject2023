import datetime
import math
import pickle

import pickle
import graph
import main
import parse_files_dict


def get_posts(username):
    statuses = parse_files_dict.load_statuses('./dataset/original_statuses.csv')
    pickle_file_path = "graph.pickle"
    with open(pickle_file_path, "rb") as file:
        graph_ = pickle.load(file)


    outgoing_edges = graph_.out_edges(username)

    potential_statuses = []
    i=0
    for source,target  in outgoing_edges:
       for status in statuses.values():
            if status['author'] == target:
                affinity = calculate_edge_rank(graph_[source][target]['weight'] , status,username,graph_)
                potential_statuses.append([status['status_id'],affinity])

    sorted_statuses = sorted(potential_statuses, key= lambda x:x[1], reverse=True)

    sorted_statuses = sorted_statuses[:10]

    for status_tuple in sorted_statuses:
        status = statuses[status_tuple[0]]
        print("☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷\n")
        print (
               str(status['status_published'])+"\n"+
               "---------------------------------------------------\n"+
               status['author']+"\n"+
               "----------------------\n"
               +status['status_message']+"\n"
               "---------------------------------------------------\n"+
               "number of reactions :" +str(status['num_reactions'])+"\n"+
               "number of comments: " + str(status['num_comments'])+"\n"
               "")
        print("☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷\n"
              ""
              ""
              "")

def calculate_edge_rank(weight,status,username,graph_):
    time_factor, content_factor,friends_factor = status_affinity(status,username,graph_)
    affinity = (weight+friends_factor) * content_factor * time_factor
    return affinity

def status_affinity(status,username,graph_):
    comment_factor = 0.6 #DA BI IOZBEGLI VELKIKE BROJEVE PRILIKOM MNOZENJA
    reaction_factor = 0.4

    content_factor = 0 #POCTNO STAVLJAMO NA NULA

    content_factor += status['num_reactions']*reaction_factor
    content_factor += status['num_comments'] *comment_factor

    time_factor = time_affinity(status['status_published'])

    friends = main.all_users[username]['friends']

    friends_factor = 0
    for friend in friends: #ZA PRIJATELJE I PRIJATELJE PRIJATELJA!
        try:
            affinity = graph_[friend][status['author']]['weight']
            if affinity > 0:
                friends_factor+=1
        except:
            continue


    return time_factor,content_factor,friends_factor


def time_affinity(date):
    current_date = datetime.date.today()
    date_of_interation = date.date()
    day_difference = (current_date - date_of_interation).days
    decay_rate = 0.03
    result = math.exp(-decay_rate * day_difference)

    return result
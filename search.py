import pickle

import parse_files_dict
import pytrie
import posts

statuses = parse_files_dict.load_statuses('./dataset/original_statuses.csv')

#HIGLIGHT
RED = '\033[91m'
RESET = '\033[0m'
STRIP_CHARACTERS = ',:!?’"'
def count_affinity(statuses_id,graph_,username):
    all_statuses = []
    for status_id in statuses_id:
        status = statuses[status_id]
        try:
            affinity = posts.calculate_edge_rank(graph_[username][status['author']]['weight'], status,username,graph_)
            all_statuses.append((status, affinity))
        except KeyError:
            affinity = posts.calculate_edge_rank(1, status,username,graph_)
            all_statuses.append((status, affinity))
    return all_statuses

def strip_characters(word, characters):
    translation_table = str.maketrans('', '', characters)
    stripped_word = word.translate(translation_table)
    return stripped_word


def search_posts(username):


    pickle_file_path = "graph.pickle"
    with open(pickle_file_path, "rb") as file:
        graph_ = pickle.load(file)

    trie = create_tree(statuses)
    while True :
        print("------------------------------------\n"
              "Za povratak nazad pritisnite X\n"
              "------------------------------------\n"
              "INSTRUCTIONS\n"
              "1) ako zelite pretraziti samo deo reci, ukucajte deo zeljene reci i stavite '*' na kraj\n"
              "2) ako zelite uneti frazu, na kraj i na pocetak teksta stavite navodnike \n"
              '---------------------------------------------------------------------------------------\n')
        post = input("Unesite zeljenu rec/deo reci/frazu:")
        if post == "x" or post=="X":
            break
        split = post.split(" ")

        if len(split)>1:
            if post.startswith('"') and post.endswith('"'):#FRAZA
                phrase = post.strip('"')
                all = []
                for status in statuses.values():
                    message = status['status_message']
                    if phrase in message:
                       all.append(status['status_id'])
                if len(all) != 0:
                    all_statuses = count_affinity(all,graph_,username)
                    print_status(all_statuses,phrase,True)
                else:
                    print("Navedena fraza ne postoji!")
            else: #VISE RECI NAVEDENIH!
                count = {}
                for word in split:
                    word = word.lower()
                    statuses_id = trie.get(word)
                    if statuses_id is None:
                        continue
                    for status_id in statuses_id:
                        status_message = statuses[status_id]['status_message'].split(" ")
                        status_messages = [word.lower() for word in status_message]
                        number = status_messages.count(word)
                        if status_id in count:
                            count[status_id] = count[status_id]+number
                        else:
                            count[status_id] = number
                if (len(count) == 0):
                    print("Ne postoje trazene reci!!")
                all_statuses = []
                for status_id in count:
                    status = statuses[status_id]
                    try:
                        affinity = count[status_id]*posts.calculate_edge_rank(graph_[username][status['author']]['weight'], status,username,graph_)
                        all_statuses.append((status, affinity))
                    except KeyError:
                        affinity = count[status_id]*posts.calculate_edge_rank(1, status,username,graph_)
                        all_statuses.append((status, affinity))
                print_status(all_statuses,split,True)
        elif len(split) == 1: #ZA RECI
            if post.endswith("*"):
                prefix_words = list(trie.keys(post.replace("*","").lower())) #POMOCU TRIE DOBIJAMO SVE MOGUCE RECI OD NAVEDENOG PREFIKSA
                if len(prefix_words) == 0: #AKO JE 0 REC NE POSTOJI
                    print("Deo reci ne postoji!")
                else:
                    all = []
                    for word in prefix_words:
                        statuses_id = trie.get(word) #VADIMO STATUSE ZA DOBIJENE RECI
                        for id in statuses_id:
                            all.append(id)
                    all = list(set(all))
                    all_statuses = count_affinity(all,graph_,username)
                    print_status(all_statuses,prefix_words,False)
            else:
                word = post.lower() #OBICNA PRETRAGA PO JEDNOJ RECI!
                statuses_id = trie.get(word)
                if statuses_id is None:
                    print("Rec nije nadjena ni u jednoj objavi!")
                else:
                    all_statuses = count_affinity(statuses_id,graph_,username)
                    print_status(all_statuses,split,False)
    return


def print_status(all_statuses,words,multiple):
    sorted_statuses = sorted(all_statuses, key= lambda x:x[1], reverse=True)
    sorted_statuses = sorted_statuses[:10]
    for items in sorted_statuses:
        status = items[0]
        message = status['status_message']
        message_content = message.split(" ")
        final = {}
        for word in message_content:
            final.update({strip_characters(word.lower(),STRIP_CHARACTERS) : strip_characters(word,STRIP_CHARACTERS)})
        colored_text = message
        if multiple:
            colored = []
            if isinstance(words,list):
                for word in words:
                    try:
                        colored_word = f"{RED}{final[word.lower()]}{RESET}"
                        colored.append([colored_word, final[word.lower()]])
                    except KeyError:
                        continue
                for color in colored:
                    colored_text = colored_text.replace(color[1],color[0])
            else:
                colored_word = f"{RED}{words}{RESET}"
                colored_text = message.replace(words,colored_word)

        else:
            for word in words:
                try:
                    colored_word = f"{RED}{final[word.lower()]}{RESET}"
                    colored_text =message.replace(final[word.lower()],colored_word)
                except KeyError:
                    continue
        print("☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷\n")
        print(
            str(status['status_published']) + "\n" +
            "---------------------------------------------------\n" +
            status['author'] + "\n" +
            "----------------------\n"
            + colored_text + "\n"
                                         "---------------------------------------------------\n" +
            "number of reactions :" + str(status['num_reactions']) + "\n" +
            "number of comments: " + str(status['num_comments']) + "\n"
                                                                   "")
        print("☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷\n"
              ""
              ""
          "")

def create_tree(statuses):
    trie = pytrie.StringTrie()
    for status in statuses.values(): #PROLAZIMO KROZ SVE STATUSE
        content_of_statuses = {}
        words = status['status_message'].split(' ') #SPLITUJEMO PO RAZMAKU

        lowercased_words = [word.lower() for word in words] #LOWERUJEMO

        for word in lowercased_words:
            if word in trie: #ZA SVAKU REC IZ STATUSA PROVERAVAMO DA LI JE VEC U STRUKTURI , AKO NIJE PRAVIMO NOVI NODE
                if  status['status_id'] not in trie[word]:
                    trie[word].append(status['status_id'])
            else:
                trie[word] = [status['status_id']]

    return trie

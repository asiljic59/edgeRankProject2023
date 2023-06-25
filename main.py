import parse_files_dict
import posts
import search

all_users = parse_files_dict.load_friends('./dataset/friends.csv')
def successful_login(username):
    while True:
        print("===========================\n")
        print("Dobrodosli nazad", username)
        print("1) Pregled objava\n"
              "2) Pretraga\n"
              "3) Izlaz\n")
        option = input("Izaberite jednu od opcija[1-3]:")
        match option:
            case '1':
                posts.get_posts(username)
            case '2':
                search.search_posts(username)
            case '3':
                return
            case other:
                print("-----------------------------\n"
                      "Neispravan unos! Pokusajte ponovo!\n"
                      "-----------------------------\n")

if __name__ == "__main__":

    while True:
        print ("Dobrodosli na nasu aplikaciju\n"
               "-----------------------------\n")
        login = input("Unesite vase korisnicko ime:")

        if login in all_users.keys():
            successful_login(login)
            break
        else:
            print("Nepostojece korisnicko ime!")

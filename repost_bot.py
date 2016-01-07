import praw
import re
import time
import os
import pickle
import traceback

LOCATION = os.path.dirname(os.path.realpath("repost_bot.py"))
OSAPREG = ".*(osap|ontario student assist|needs? money).*"
PEYREG = ".*(pey | pey|professional exper|intern |internship).*"
COLLEGEREG = ".*(college app|for college|vic |victoria|new college|innis|trinity|uc |university college|ww |woodsworth).*"
MENTALREG = ".*(mental.+help|help.+mental|mental breakdown|depress|anxiety).*"
SOCIALREG = ".*((social(?! sci))|introvert).*"
CSENGREG = ".*(computer science| cs ).+easy.+engineer.*"

REGEXS = [MENTALREG, SOCIALREG, OSAPREG, PEYREG, COLLEGEREG, CSENGREG]


reg_to_links = {}
for regex in REGEXS:
    reg_to_links[regex] = []
reg_to_limit = {}

for regex in REGEXS:
    reg_to_limit[regex] = 5

link_to_description = {}

regex_to_comment = {
MENTALREG: "\"mental health help\"",
SOCIALREG: "\"social life in uoft\"",
OSAPREG: "\"OSAP(Ontario Student Assistant Program) questions\"",
PEYREG: "\"PEY(Professional Experience Year) questions\"",
COLLEGEREG: "\"College and residence questions\"",
CSENGREG: "\"COMP ENG > CS REKT CS KIDS\""
}

commented = set()

def read_from_files():
    global commented
    read_from_file("osap.txt", OSAPREG)
    read_from_file("pey.txt", PEYREG)
    read_from_file("college.txt", COLLEGEREG)
    read_from_file("mental.txt", MENTALREG)
    read_from_file("social.txt", SOCIALREG)
    read_from_file("cseng.txt", CSENGREG)
    try:
        commented = pickle.load(open( "commented.p", "rb" ))
        print(len(commented))
    except:
        print("no file yet")

def read_from_file(file_name, regex):
    global reg_to_links, link_to_description
    file = open("{}/{}".format(LOCATION, file_name), 'r').read().strip()
    lines = file.split("\n")
    for line in lines:
        link, des = line.split(",")
        reg_to_links[regex].append(link)
        link_to_description[link] = des
def add_link():
    return

'''
this method generates the bot's comment
'''
def get_comment(limit, post_type, links):
    result = ""
    result += "Hello OP, your post has been catogorized into the common topic {}. ".format(regex_to_comment[post_type])
    result += "Here are some old posts that you may find helpful\n\n"
    for i in range(min(limit, len(links))):
        result += "[{}]({})\n\n".format(link_to_description[links[i]], links[i])
    
    result += "If none of the posts matches your question, you could also use the search bar to find if a similar quesition has been answered before\n\n"
    result += "I am a bot, **beep boop**"
    return result

'''
this method checks match for a generic regex
'''
def check_reg_match(post, regex, limit):
    global commented
    title_match = re.match(regex, post.title.lower())
    content_match = re.match(regex, post.selftext.lower().replace("\n"," "))
    if title_match or content_match:
        #print(get_comment(limit, regex, reg_to_links[regex]))
        post.add_comment(get_comment(limit, regex, reg_to_links[regex]))
        #print(regex + " topic")
        print("replied")
        commented.add(post.id)
        return True
    return False
        
'''
this method checks for all the possible topics
'''
def check_all(post):
    for regex in REGEXS:
        if check_reg_match(post, regex, reg_to_limit[regex]):
            return

        

USERNAME = "uoft_repost_bot"
PASSWORD = "123456"
r = praw.Reddit(user_agent = "testing")
r.login(USERNAME, "123456", disable_warning=True)

def main():
    subreddit = r.get_subreddit("uoft")
    posts = subreddit.get_new(limit=5)
    for post in posts:
        if post.id not in commented:
            check_all(post)
    print("done cycle")


if __name__ == "__main__":
    read_from_files()
    
    while True:
        try:
            main()
        except:
            pickle.dump(commented, open( "commented.p", "wb" ))
            traceback.print_exc()
            break
        time.sleep(20)

#break
    
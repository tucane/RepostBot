import praw
import re
import time
import os

LOCATION = os.path.dirname(os.path.realpath("repost_bot.py"))
OSAPREG = "o"
PEYREG = "p"
COLLEGEREG = "c" 
MENTALREG = "m"
SOCIALREG = "s"
CSENGREG = "cs"
REGEXS = [OSAPREG,
          PEYREG,
          COLLEGEREG,
          MENTALREG,
          SOCIALREG,
          CSENGREG]

reg_to_links = {}
for regex in REGEXS:
    reg_to_links[regex] = []

link_to_description = {}


def read_from_files():
    read_from_file("osap.txt", OSAPREG)
    read_from_file("pey.txt", PEYREG)
    read_from_file("college.txt", COLLEGEREG)
    read_from_file("mental.txt", MENTALREG)
    read_from_file("social.txt", SOCIALREG)
    read_from_file("cseng.txt", CSENGREG)    

def read_from_file(file_name, regex):
    file = open("{}/{}".format(LOCATION, file_name), 'r').read().strip()
    lines = file.split("\n")
    for line in lines:
        link, des = line.split(",")
        reg_to_links[regex].append(link)
        link_to_description[link] = des
                

def add_link():
    return

def get_comment(limit, post_type, links):
    result = ""
    result += "Hello OP, here are some old posts that you may find useful\n\n"
    for i in range(min(limit, len(links))):
        result += "[{}]({}) ".format(link_to_description[links[i]], links[i])
    
    result += "\n\n I am a bot, **beep boop**"
    return result

'''
checking if the post has a similar topic to the followings:
'''

def check_OSAP(post):
    return check_reg_match(post, OSAPREG, 5)

def check_PEY(post):
    return check_reg_match(post, PEYREG, 5)

def check_college(post):
    return check_reg_match(post, COLLEGEREG, 5)

def check_mental(post):
    return check_reg_match(post, MENTALREG, 5)

def check_social(post):
    return check_reg_match(post, SOCIALREG, 5)

def check_cseng(post):
    return check_reg_match(post, CSENGREG, 10)

'''
'''
def check_reg_match(post, regex, limit):
    title_match = re.match(regex, post.title.lower())
    content.match = re.match(regex, post.body.lower())
    if title_match or content_match:
        post.add_comment(get_comment(limit, regex, reg_to_links[regex]))
        print(regex + " topic")
        return True
    return False
        

def check_all(post):
    if not check_mental():
        if not check_social():
            if not check_OSAP():
                if not check_PEY():
                    if not check_college():
                        check_cseng()

        

USERNAME = "bad_uoft_repost_bot"
PASSWORD = "123456"
r = praw.Reddit(user_agent = "testing")
r.login(USERNAME, "123456", disable_warning=True)

def main():
    subreddit = r.get_subreddit("testingground4bots")
    post = subreddit.get_new(limit=1)
    for post in posts:
        check_all(post)


if __name__ == "__main__":
    read_from_files()
    '''
    while True:
        time.sleep(1)
        main()
    '''
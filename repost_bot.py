import praw
import re
import time
import os

LOCATION = os.path.dirname(os.path.realpath("repost_bot.py"))
OSAPREG = ".*(osap|ontario student assist|needs? money).*"
PEYREG = ".*( pey |professional exper|intern).*"
COLLEGEREG = ".*(college app|for college|vic |victoria|new college|innis|trinity|uc |university college|ww |woodsworth).*"
MENTALREG = ".*(mental.+help|help.+mental|depress|anxiety).*"
SOCIALREG = ".*(social ^(science)|introvert).*"
CSENGREG = ".*(computer science| cs ).+easy.*"

REGEXS = [MENTALREG, SOCIALREG, OSAPREG, PEYREG, COLLEGEREG, CSENGREG]

reg_to_links = {}
for regex in REGEXS:
    reg_to_links[regex] = []
reg_to_limit = {}

for regex in REGEXS:
    reg_to_limit[regex] = 5

link_to_description = {}
commented = set()

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

'''
this method generates the bot's comment
'''
def get_comment(limit, post_type, links):
    result = ""
    result += "Hello OP, here are some old posts that you may find useful\n\n"
    for i in range(min(limit, len(links))):
        result += "[{}]({})\n\n".format(link_to_description[links[i]], links[i])
    
    result += "\n\nI am a bot, **beep boop**"
    return result

'''
this method checks match for a generic regex
'''
def check_reg_match(post, regex, limit):
    title_match = re.match(regex, post.title.lower())
    content_match = re.match(regex, post.selftext.lower())
    if title_match or content_match:
        print(get_comment(limit, regex, reg_to_links[regex]))
        post.add_comment(get_comment(limit, regex, reg_to_links[regex]))
        print(regex + " topic")
        commented.add(post)
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
    subreddit = r.get_subreddit("testingground4bots")
    posts = subreddit.get_new(limit=1)
    for post in posts:
        if post not in commented:
            check_all(post)


if __name__ == "__main__":
    read_from_files()
    
    while True:
        main()
        time.sleep(10)
#break
    
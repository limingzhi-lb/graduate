import itchat
from itchat.content import *

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])


# itchat.auto_login(hotReload=True)
# itchat.auto_login()

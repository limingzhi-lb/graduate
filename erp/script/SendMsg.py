import itchat
from InfoManage.config import Config
from django.contrib.auth.models import Group
config = Config()


class SendMsg(object):
    def __init__(self, group, msg):
        group = Group.objects.get(name=group)
        self.msg = msg
        user = group.user_set.all()
        self.user = user.get(is_leader=True)
        self.check = False

    def send(self):
        users = itchat.search_friends(name=self.user.username)
        if users:
            userName = users[0]['UserName']
            itchat.send(self.msg, toUserName=userName)

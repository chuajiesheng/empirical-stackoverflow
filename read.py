from xml.dom import minidom


class User:
    user_id = None
    questions = 0
    answers = 0

    def __init__(self, user_id):
        self.user_id = user_id

    def output(self):
        return '{}, {}, {}'.format(self.user_id, self.questions, self.answers)

users = dict()

doc = minidom.parse('data/dataset.xml')
items = doc.getElementsByTagName('row')

for item in items:
    keys = item.attributes.keys()
    user_id = None
    if 'OwnerUserId' in keys:
        user_id = item.attributes['OwnerUserId'].value
    elif 'LastEditorUserId' in keys:
        user_id = item.attributes['LastEditorUserId'].value

    user = None
    if user_id not in users.keys():
        user = User(user_id)
    else:
        user = users.get(user_id)

    post_type = item.attributes['PostTypeId'].value

    if post_type == '1':
        user.questions += 1
    elif post_type == '2':
        user.answers += 1

    users[user_id] = user

for key, user in users.iteritems():
    print user.output()


from xml.dom import minidom


class User:
    user_id = None
    questions = 0
    answers = 0

    def __init__(self, user_id):
        self.user_id = user_id

    def output(self):
        return '{}, {}, {}'.format(self.user_id, self.questions, self.answers)

class Question:
    question_id = None
    item = None
    answers = []

    def __init__(self, question_id, item):
        self.question_id = question_id
        self.item = item

    def add_answer(self, answer):
        self.answers.append(answer)


class Answer:
    answer_id = None
    item = None

    def __init__(self, answer_id, item):
        self.answer_id = answer_id
        self.item = item


def print_user_csv(users):
    print 'user, questions_asked, questions_answered'
    for key, user in users.iteritems():
        print user.output()


users = dict()
questions = dict()
row_with_no_user_id = 0

doc = minidom.parse('data/dataset.xml')
items = doc.getElementsByTagName('row')

for item in items:
    keys = item.attributes.keys()

    user_id = None
    if 'OwnerUserId' in keys:
        user_id = item.attributes['OwnerUserId'].value
    elif 'LastEditorUserId' in keys:
        user_id = item.attributes['LastEditorUserId'].value

    if user_id is None:
        row_with_no_user_id += 1
        # print item.attributes.keys()

    user = None

    if user_id not in users.keys():
        user = User(user_id)
    else:
        user = users.get(user_id)

    post_type = item.attributes['PostTypeId'].value

    if post_type == '1': # question
        user.questions += 1

        question_id = item.attributes['Id'].value
        question = Question(question_id, item)
        questions[question_id] = question

    elif post_type == '2': # answer
        user.answers += 1

        question_id = item.attributes['ParentId'].value
        answer = Answer(item.attributes['Id'], item)

        if question_id in questions.keys():
            questions[question_id].add_answer(answer)
        else:
            # print question_id, 'not found'
            pass

    users[user_id] = user

# print row_with_no_user_id, 'rows with no id'
# print_user_csv(users)


from xml.dom import minidom
import dateutil.parser


class User:
    user_id = None
    questions = 0
    answers = 0

    def __init__(self, user_id):
        self.user_id = user_id

    def output(self):
        return '{}, {}, {}'.format(self.user_id, self.questions, self.answers)

class Question:
    item = None
    question_id = None
    accepted_answer_id = None
    answers = []

    def __init__(self, item):
        self.item = item
        self.question_id = item.attributes['Id'].value
        if 'AcceptedAnswerId' in item.attributes.keys():
            self.accepted_answer_id = item.attributes['AcceptedAnswerId'].value

    def get_poster(self):
        if 'OwnerUserId' in self.item.attributes.keys():
            return self.item.attributes['OwnerUserId'].value
        elif 'LastEditorUserId' in keys:
            return self.item.attributes['LastEditorUserId'].value

        return None

    def add_answer(self, answer):
        self.answers.append(answer)

    def print_poster_answerer_id(self):
        for a in self.answers:
            if a.answer_id == self.accepted_answer_id:
                if self.get_poster() is None or a.get_poster() is None:
                    print self.get_poster(), '-', a.get_poster()
                elif int(self.get_poster()) < int(a.get_poster()):
                    print self.get_poster() + ' i - ', a.get_poster() + ' a'
                else:
                    print a.get_poster() + ' a - ', self.get_poster() + ' i'
                return


class Answer:
    item = None
    answer_id = None

    def __init__(self, item):
        self.item = item
        self.answer_id = item.attributes['Id'].value

    def get_poster(self):
        if 'OwnerUserId' in self.item.attributes.keys():
            return self.item.attributes['OwnerUserId'].value
        elif 'LastEditorUserId' in keys:
            return self.item.attributes['LastEditorUserId'].value

        return None


def print_user_csv(users):
    print 'user, questions_asked, questions_answered'
    for key, user in users.iteritems():
        print user.output()


def get_hour_distribution(dictionary):
    d = dateutil.parser.parse(creation_date)
    if str(d.hour) not in dictionary.keys():
        dictionary[str(d.hour)] = 1
    else:
        dictionary[str(d.hour)] += 1


users = dict()
questions = dict()
hours = dict()
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

    creation_date = item.attributes['CreationDate'].value
    get_hour_distribution(hours)

    post_type = item.attributes['PostTypeId'].value

    if post_type == '1': # question
        user.questions += 1

        question_id = item.attributes['Id'].value
        question = Question(item)
        questions[question_id] = question

    elif post_type == '2': # answer
        user.answers += 1

        question_id = item.attributes['ParentId'].value
        answer = Answer(item)

        if question_id in questions.keys():
            questions[question_id].add_answer(answer)
        else:
            # print question_id, 'not found'
            pass

    users[user_id] = user

# print row_with_no_user_id, 'rows with no id'
# print_user_csv(users)
for k, q in questions.iteritems():
    # q.print_poster_answerer_id()
    pass

print 'hour, posts'
for k, v in hours.iteritems():
    print k, ',', v
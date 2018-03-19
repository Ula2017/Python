from random import randint
from analyzer.Exception import OnlyLiesSpeaking
import datetime
from datetime import date


class LieDetector:

    def __init__(self):
        self.information = []
        self.lies_level = 0

    def read_file(self):
        path = './question.txt'
        questions_file = open(path, 'r')
        result = questions_file.read()
        questions_file.close()
        return result

    def get_information(self, quest):
        print("Answer the questions carefully and honestly\n")
        for i in range(0, 5):
            print(quest[i])
            print('\n')
            ans = input()
            self.information.append(ans)
        return self.information

    def rand_question_to_print(self, asked):
        i = 0
        counter = 0
        while asked[i] != -1 and counter < 30:
            i = randint(5, 33)
            counter += 1
        if asked[i] == 0:
            for x in asked:
                if asked[x] == -1:
                    return x
            return -1
        else:
            return i

    def check_month_day(self, day, month):
        m = [(1, 31), (2, 28), (3, 31), (4, 30), (5, 31), (6, 30),
             (7, 31), (8, 31), (9, 30), (10, 31), (11, 30), (12, 31)]
        if m[month - 1][1] < day or month <= 0 or month > 12 or day < 1:
            return -1
        return 0

    def check_date(self, string):
        now = datetime.datetime.now()
        dates = string.split('-')
        try:
            if len(dates) != 3:
                raise OnlyLiesSpeaking
            dates[0] = int(dates[0])
            dates[1] = int(dates[1])
            dates[2] = int(dates[2])
            if self.check_month_day(
                    dates[0],
                    dates[1]) == -1 or dates[2] >= now.year or dates[2] <= 1900:
                raise OnlyLiesSpeaking

        except OnlyLiesSpeaking:
            raise
        except ValueError:
            raise OnlyLiesSpeaking

    def has_numbers(self, input_string):
        return any(char.isdigit() for char in input_string)

    def check_if_true(self, info):

        i = 0
        for _ in info:
            if i != 1:
                try:
                    if self.has_numbers(info[i]):
                        raise OnlyLiesSpeaking
                except OnlyLiesSpeaking:
                    raise
            i += 1
        self.check_date(info[1])

    def calculate_age(self, born):
        today = date.today()
        try:
            birthday = born.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(
                year=today.year, month=born.month + 1, day=1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def weekday(self, number):
        return {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }[number]

    def months(self, m):
        return {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }[m]

    def complete_question(self, question, details):

        dates = details[1].split('-')
        now = datetime.datetime.now()
        answer = 2
        if question.find('<name>') != -1:
            result = question[:-7]
            result += details[0]
            answer = 1
        elif question.find('<tname>') != -1:
            result = question[:-8]
            name = details[0]
            if len(name) > 3:
                i = randint(1, len(name))
                j = randint(1, len(name))
                while i == j:
                    j = randint(1, len(name) - 1)
                tmp = name[i]
                name[i] = name[j]
                name[j] = tmp
                answer = 0
            else:
                answer = 1
            result += name
        elif question.find('<year>') != -1:
            result = question[:-7]
            result += dates[2]
            answer = 1
        elif question.find('<tyear>') != -1:
            result = question[:-8]
            d = int(dates[2]) - 1
            result += str(d)
            answer = 0
        elif question.find('<month>') != -1:
            result = question[:-8]
            result += self.months(int(dates[1]))
            answer = 1
        elif question.find('<date>') != -1:
            result = question[:-7]
            result += details[1]
            answer = 1
        elif question.find('<mother>') != -1:
            result = question[:-9]
            result += details[2]
            answer = 1
        elif question.find('<father>') != -1:
            result = question[:-10]
            result += details[4]
            answer = 0
        elif question.find('<hours>') != -1:
            result = question[:-8]
            result += str(now.hour)
            answer = 1
        elif question.find('<thours>') != -1:
            result = question[:-9]
            result += str(now.hour - 1)
            answer = 0
        elif question.find('<actual>') != -1:
            result = question[:-9]
            s = self.weekday(datetime.datetime.now().weekday())
            result += s
            answer = 1
        elif question.find('<tactual>') != -1:
            result = question[:-10]
            i = datetime.datetime.now().weekday() + 1
            result += self.weekday(i)
            answer = 0
        elif question.find('<age>') != -1:
            result = question[:-15]
            result += str(self.calculate_age(datetime.date(
                int(dates[2]), int(dates[1]), int(dates[0]))))
            result += ' year old'
            answer = 1
        elif question.find('<tage>') != -1:
            result = question[:-16]
            result += str(self.calculate_age(datetime.date(
                int(dates[2]), int(dates[1]), int(dates[0]))) - 1)
            result += ' year old'
            answer = 0
        result += '?'
        return result, answer

    def truth_analyzer(self, result):
        l = 0
        tmp = [2, 2, 2, 2, 2]
        for q in result:
            if q[0].find('g1.') != -1 and q[1] == 1:
                l += 1
            if q[0].find('f1.') != -1 and q[1] == 0:
                l += 1
            if q[0].find('h1.') != -1 and q[1] == 1:
                l += 1
            if q[0].find('e1.') != -1 and q[1] == 0:
                l += 1
            if q[0].find('a5.') != -1:
                tmp[4] = q[1]
            if q[0].find('a1.') != -1:
                tmp[0] = q[1]
            if q[0].find('a2.') != -1:
                tmp[1] = q[1]
            if q[0].find('a3.') != -1:
                tmp[2] = q[1]
            if q[0].find('a4.') != -1:
                tmp[3] = q[1]

        if tmp[2] == 0 and any(True for x in tmp if x == 1):
            l += 2
        elif tmp[1] == 1 and tmp[0] != 1:
            l += 1
        elif tmp[4] == 1 and tmp[3] != 1:
            l += 1

        self.lies_level += l
        return l / len(result)

    def ask_simply_question(self, quest):

        asked = [-1 for x in range(35)]
        i = 0
        result = []
        while i != 5:
            asked[i] = 0
            i += 1
        i = 0
        question = quest.split('\n')

        info = self.get_information(question)
        self.check_if_true(info)
        rand = 1
        while bool(rand):
            num = self.rand_question_to_print(asked)
            if num == -1:
                rand = 0
            else:
                asked[num] = 0
                i += 1
                # we have to prepere question to asked before asked
                if question[num].find('<') != -1:
                    prepared = self.complete_question(question[num], info)
                else:
                    q = question[num]
                    prepared = []
                    prepared.append(q[3:])
                    prepared.append(-1)
                print(prepared[0])
                print('\n')
                ans = input()
                try:
                    ans = int(ans)
                    if ans != 0 and ans != 1:
                        raise OnlyLiesSpeaking
                    if prepared[1] != -1 and prepared[1] != ans:
                        self.lies_level += 1
                except ValueError:
                    raise OnlyLiesSpeaking
                except OnlyLiesSpeaking:
                    raise
                if prepared[1] == -1:
                    result.append((question[num], ans))
        level = self.lies_level / i
        level += self.truth_analyzer(result)
        level /= 2
        return level

    def do_search(self):
        question_string = self.read_file()
        level = self.ask_simply_question(question_string)
        level *= 100
        if level > 10:
            print("LIEDETECTOR: The sentence is probably false.")
        else:
            print("LIEDETECTOR: The sentence is probably true.")

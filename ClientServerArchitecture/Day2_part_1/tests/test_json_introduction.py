import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json_introduction as js
import unittest


class TestJsonFunctions(unittest.TestCase):
    def test_parse_empty_json(self):
        self.assertEqual(js.parse_json("{}"), {})

    def test_parse_one_field_json(self):
        self.assertEqual(js.parse_json('{"name":"no_name"}'), {"name": "no_name"})

    def test_parse_coordinates(self):
        self.assertEqual(js.parse_json('{"lat": 43.3212, "lon": 43.112}'),
                         {"lat": 43.3212, "lon": 43.112})


    def test_construct_empty_json(self):
        self.assertEqual("{}", js.construct_json({}))

    def test_construct_one_field_json(self):
        self.assertEqual('{"name": "no_name"}', js.construct_json({"name": "no_name"}))

    def test_construct_coordinates(self):
        self.assertEqual('{"lat": 43.3212, "lon": 43.112}',
                         js.construct_json({"lat": 43.3212, "lon": 43.112}))


    def test_coordiantes_construct(self):
        self.assertEqual(json.loads(js.construct_coordinates(0.5, 0.6)), {"lon": 0.5, "lat": 0.6})
        self.assertEqual(json.loads(js.construct_coordinates(0.3, 1.6)), {"lon": 0.3, "lat": 1.6})


    def test_names_construct(self):
        self.assertEqual(json.loads(js.construct_names(["Alpha", "Betta", "Gamma"])),
                         {"names": ["Alpha", "Betta", "Gamma"]})
        self.assertEqual(json.loads(js.construct_names(["alpha", "betta", "gamma"])),
                         {"names": []})
        self.assertEqual(json.loads(js.construct_names([])),
                         {"names": []})
        self.assertEqual(json.loads(js.construct_names(["alpha", "Betta", "gamma"])),
                         {"names": ["Betta"]})
        self.assertEqual(json.loads(js.construct_names(["Alpha", "betta", "Gamma"])),
                         {"names": ["Alpha", "Gamma"]})


    def test_string_group(self):
        self.assertEqual(json.loads(js.group_strings(["Alpha", "Betta", "Gamma"])),
                         {
                             "A": ["Alpha"],
                             "B": ["Betta"],
                             "G": ["Gamma"],
                         })
        self.assertEqual(json.loads(js.group_strings(["123", "1asd", "XAS"])),
                         {
                             "1": ["123", "1asd"],
                             "X": ["XAS"],
                         })


    def test_long_names(self):
        self.assertEqual(js.extract_long_names({
            "names": [
                "Tom",
                "Rik",
                "Albert",
                "Camille"
            ]
        }), ["Albert", "Camille"])
        self.assertEqual(js.extract_long_names({
            "names": [
                "Tomas",
                "Rikardo"
            ]
        }), ["Rikardo"])
        self.assertEqual(js.extract_long_names({
            "wrong key": [
                "Tomas",
                "Rikardo"
            ]
        }), [])


    def test_count_word(self):
        self.assertEqual(
            js.count_words(""" I'll be back!! """),
            {"i'll": 1, 'be': 1, 'back': 1})

        self.assertEqual(
            js.count_words("""
    You shall have no other gods before Me.
    You shall not make idols.
    You shall not take the name of the LORD your God in vain.
    Remember the Sabbath day, to keep it holy.
    Honor your father and your mother.
    You shall not murder.
    You shall not commit adultery.
    You shall not steal.
    You shall not bear false witness against your neighbor.
    You shall not covet.!
    """),
            {
                'and': 1,
                'the': 3,
                'murder': 1,
                'false': 1,
                'adultery': 1,
                'holy': 1,
                'shall': 8,
                'gods': 1,
                'vain': 1,
                'mother': 1,
                'covet': 1,
                'it': 1,
                'sabbath': 1,
                'not': 7,
                'bear': 1,
                'have': 1,
                'in': 1,
                'idols': 1,
                'keep': 1,
                'your': 4,
                'witness': 1,
                'remember': 1,
                'me': 1,
                'name': 1,
                'no': 1,
                'god': 1,
                'make': 1,
                'commit': 1,
                'father': 1,
                'against': 1,
                'day': 1,
                'to': 1,
                'other': 1,
                'take': 1,
                'neighbor': 1,
                'of': 1,
                'lord': 1,
                'you': 8,
                'before': 1,
                'steal': 1,
                'honor': 1
            })

        self.assertEqual(
            js.count_words(""" Frequently asked questions (FAQ) or Questions and Answers (Q&A), are listed questions
            and answers, all supposed to be commonly asked in some context, and pertaining to a particular topic.
            The format is commonly used on email mailing lists and other online forums, where certain common questions
            tend to recur.
            "FAQ" is pronounced as either an initialism (F-A-Q) or an acronym. Since the acronym FAQ originated in
            textual media, its pronunciation varies; "F-A-Q",[1] is commonly heard.
            Depending on usage, the term may refer specifically to a single frequently asked question,
            or to an assembled list of many questions and their answers. Web page designers often label a single list
            of questions as a "FAQ", such as on Google.com,[2] while using "FAQs"
            to denote multiple lists of questions such as on United States Treasury sites. """),
            {
                'assembled': 1,
                'all': 1,
                'specifically': 1,
                'questions': 7,
                'frequently': 2,
                'tend': 1,
                'forums': 1,
                'its': 1,
                'varies;': 1,
                'web': 1,
                'designers': 1,
                'recur': 1,
                'to': 6,
                'question': 1,
                'textual': 1,
                'their': 1,
                'pronunciation': 1,
                'listed': 1,
                'treasury': 1,
                'usage': 1,
                'initialism': 1,
                'format': 1,
                'faq': 4,
                'lists': 2,
                'particular': 1,
                'using': 1,
                'denote': 1,
                'common': 1,
                'states': 1,
                'term': 1,
                'f': 2,
                'list': 2,
                'single': 2,
                'email': 1,
                'while': 1,
                'either': 1,
                '[2]': 1,
                'refer': 1,
                'where': 1,
                'page': 1,
                '[1]': 1,
                'and': 5,
                'pertaining': 1,
                'google': 1,
                'often': 1,
                'certain': 1,
                'is': 3,
                'some': 1,
                'an': 3,
                'topic': 1,
                'heard': 1,
                'as': 4,
                'are': 1,
                'in': 2,
                'pronounced': 1,
                'united': 1,
                'depending': 1,
                'media': 1,
                'since': 1,
                'sites': 1,
                'faqs': 1,
                'label': 1,
                'acronym': 2,
                'other': 1,
                'online': 1,
                'many': 1,
                'q&a': 1,
                'supposed': 1,
                'be': 1,
                'used': 1,
                'multiple': 1,
                'may': 1,
                'of': 3,
                'answers': 3,
                'such': 2,
                'originated': 1,
                'a': 6,
                'on': 4,
                'mailing': 1,
                'commonly': 3,
                'asked': 3,
                'q': 2,
                'context': 1,
                'the': 3,
                'com': 1,
                'or': 3
            })

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestJsonFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)

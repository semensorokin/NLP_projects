# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import regexp_introduction as regexp
import unittest


class TestRegularExpressions(unittest.TestCase):
    def test_match_three_letters(self):
        self.assertTrue(regexp.match_three_letters("123"))
        self.assertTrue(regexp.match_three_letters("asd"))
        self.assertTrue(regexp.match_three_letters("+--"))
        self.assertTrue(regexp.match_three_letters("!\t#"))
        self.assertFalse(regexp.match_three_letters("as"))
        self.assertFalse(regexp.match_three_letters("asas"))

    def test_match_a_smth_b(self):
        self.assertTrue(regexp.match_a_smth_b("abc"))
        self.assertTrue(regexp.match_a_smth_b("a4c"))
        self.assertTrue(regexp.match_a_smth_b("a!c"))
        self.assertFalse(regexp.match_a_smth_b("abb"))
        self.assertFalse(regexp.match_a_smth_b("bbc"))
        self.assertFalse(regexp.match_a_smth_b("abbc"))

    def test_match_long_seq(self):
        self.assertTrue(regexp.match_long_seq("abc"))
        self.assertTrue(regexp.match_long_seq("abbc"))
        self.assertTrue(regexp.match_long_seq("abbbbbc"))
        self.assertFalse(regexp.match_long_seq("abbbbb"))
        self.assertFalse(regexp.match_long_seq("affc"))
        self.assertFalse(regexp.match_long_seq("ac"))

    def test_match_letters_between(self):
        self.assertTrue(regexp.match_letters_between("abba"))
        self.assertTrue(regexp.match_letters_between("abbbba"))
        self.assertTrue(regexp.match_letters_between("abbkba"))
        self.assertTrue(regexp.match_letters_between("abbbbbbbba"))
        self.assertFalse(regexp.match_letters_between("bbb"))
        self.assertFalse(regexp.match_letters_between("aa"))
        self.assertTrue(regexp.match_letters_between("aabba"))

    def test_match_doc_file(self):
        self.assertTrue(regexp.match_doc_file("qasd.doc"))
        self.assertTrue(regexp.match_doc_file("QswwwdD.doc"))
        self.assertTrue(regexp.match_doc_file("abbbbbc..doc"))
        self.assertFalse(regexp.match_doc_file("abbbbb.edoc"))
        self.assertFalse(regexp.match_doc_file("affc.docx"))
        self.assertFalse(regexp.match_doc_file("ac.doc."))
        self.assertTrue(regexp.match_docx_file(".doc"))
        self.assertFalse(regexp.match_doc_file("abbbbbdoc"))

    def test_match_docx_file(self):
        self.assertTrue(regexp.match_docx_file("qasd.doc"))
        self.assertTrue(regexp.match_docx_file("QswwwdD.doc"))
        self.assertTrue(regexp.match_docx_file("abbbbbc..doc"))
        self.assertFalse(regexp.match_docx_file("abbbbb.edoc"))
        self.assertTrue(regexp.match_docx_file("affc.docx"))
        self.assertFalse(regexp.match_docx_file("ac.doc."))
        self.assertFalse(regexp.match_docx_file("ac.doc.docxx"))
        self.assertTrue(regexp.match_docx_file(".docx"))
        self.assertFalse(regexp.match_doc_file("abbbbbdocx"))

    def test_match_nonempty_docx_file(self):
        self.assertTrue(regexp.match_nonempty_docx_file("qasd.doc"))
        self.assertTrue(regexp.match_nonempty_docx_file("QswwwdD.doc"))
        self.assertTrue(regexp.match_nonempty_docx_file("abbbbbc..doc"))
        self.assertFalse(regexp.match_nonempty_docx_file("abbbbb.edoc"))
        self.assertTrue(regexp.match_nonempty_docx_file("affc.docx"))
        self.assertFalse(regexp.match_nonempty_docx_file("ac.doc."))
        self.assertFalse(regexp.match_nonempty_docx_file("ac.doc.docxx"))
        self.assertFalse(regexp.match_nonempty_docx_file(".docx"))
        self.assertFalse(regexp.match_doc_file("abbbbbdocx"))

    def test_match_find_many_names(self):
        self.assertTrue(regexp.match_find_many_names("lala name name lala name"))
        self.assertTrue(regexp.match_find_many_names("name this string is about name"))
        self.assertTrue(regexp.match_find_many_names("name nameqwerty"))
        self.assertFalse(regexp.match_find_many_names("qwerty name"))
        self.assertTrue(regexp.match_find_many_names("nnnnnnname name"))
        self.assertFalse(regexp.match_find_many_names("programmer name"))
        self.assertFalse(regexp.match_find_many_names("progra5mmer"))

    def test_match_pavel_sukhov(self):
        self.assertTrue(regexp.match_pavel_sukhov("Pavel Sukhov"))
        self.assertTrue(regexp.match_pavel_sukhov("pavel sukhov"))
        self.assertTrue(regexp.match_pavel_sukhov("Pavel sukhov"))
        self.assertTrue(regexp.match_pavel_sukhov("pavel Sukhov"))
        self.assertFalse(regexp.match_pavel_sukhov("Pavel SUkhov"))
        self.assertFalse(regexp.match_pavel_sukhov("Pavel SuKhov"))
        self.assertFalse(regexp.match_pavel_sukhov("pavel sukho"))
        self.assertFalse(regexp.match_pavel_sukhov("avel Sukhov"))
        self.assertFalse(regexp.match_pavel_sukhov("PavelSukhov"))

    def test_match_vowels(self):
        self.assertTrue(regexp.match_vowels("eyuioa"))
        self.assertTrue(regexp.match_vowels("ey"))
        self.assertTrue(regexp.match_vowels("uioa"))
        self.assertTrue(regexp.match_vowels("ioaeyu"))
        self.assertTrue(regexp.match_vowels("eyuoa"))
        self.assertTrue(regexp.match_vowels("AEYUOI"))
        self.assertTrue(regexp.match_vowels("aeyuoiAEYUOI"))
        self.assertTrue(regexp.match_vowels("Aa"))
        self.assertFalse(regexp.match_vowels("eyuioa,"))
        self.assertFalse(regexp.match_vowels("-eyuioa"))
        self.assertFalse(regexp.match_vowels("Peyuioa,"))
        self.assertFalse(regexp.match_vowels("Pepe"))
        self.assertFalse(regexp.match_vowels("zoo"))
        self.assertFalse(regexp.match_vowels("1a"))
        self.assertFalse(regexp.match_vowels("a5"))
        self.assertFalse(regexp.match_vowels(""))


    def test_match_no_vowels(self):
        self.assertTrue(regexp.match_no_vowels("swd"))
        self.assertTrue(regexp.match_no_vowels("bdsm"))
        self.assertTrue(regexp.match_no_vowels("123"))
        self.assertTrue(regexp.match_no_vowels("!@#$"))
        self.assertTrue(regexp.match_no_vowels("^!"))
        self.assertTrue(regexp.match_no_vowels("Q"))
        self.assertTrue(regexp.match_no_vowels("qw3rt"))
        self.assertTrue(regexp.match_no_vowels(""))
        self.assertFalse(regexp.match_no_vowels("Kalipso"))
        self.assertFalse(regexp.match_no_vowels("alps"))
        self.assertFalse(regexp.match_no_vowels("ae123"))
        self.assertFalse(regexp.match_no_vowels("bla"))
        self.assertFalse(regexp.match_no_vowels("bla-bla"))


    def test_match_alphabet_order(self):
        self.assertTrue(regexp.match_alphabet_order("abc"))
        self.assertTrue(regexp.match_alphabet_order("abcdefghijk"))
        self.assertTrue(regexp.match_alphabet_order("abdfkmnpstvxz"))
        self.assertTrue(regexp.match_alphabet_order("cxy"))
        self.assertTrue(regexp.match_alphabet_order("cdklstxy"))
        self.assertTrue(regexp.match_alphabet_order("bfrtw"))
        self.assertTrue(regexp.match_alphabet_order("a b c"))
        self.assertTrue(regexp.match_alphabet_order("acg jko pr"))
        self.assertTrue(regexp.match_alphabet_order("a z"))
        self.assertTrue(regexp.match_alphabet_order("v  z"))
        self.assertTrue(regexp.match_alphabet_order("a  b cdefg kl"))
        self.assertTrue(regexp.match_alphabet_order("uv xyz"))
        self.assertTrue(regexp.match_alphabet_order("ab de gh"))
        self.assertTrue(regexp.match_alphabet_order("x yz"))
        self.assertTrue(regexp.match_alphabet_order("abcdefghijklmnopqrstuvwxyz"))
        self.assertFalse(regexp.match_alphabet_order("abbc"))
        self.assertFalse(regexp.match_alphabet_order("abcb"))
        self.assertFalse(regexp.match_alphabet_order("a bcdjkrza"))
        self.assertFalse(regexp.match_alphabet_order("qwerty"))
        self.assertFalse(regexp.match_alphabet_order("zyxcba"))
        self.assertFalse(regexp.match_alphabet_order("abcdfe"))
        self.assertFalse(regexp.match_alphabet_order("ab c dfe"))
        self.assertFalse(regexp.match_alphabet_order("a  z  a"))
        self.assertFalse(regexp.match_alphabet_order("asdfg"))
        self.assertFalse(regexp.match_alphabet_order("asd  f g"))
        self.assertFalse(regexp.match_alphabet_order("poqwoieruytjhfg"))

    def test_match_id_address(self):
        self.assertTrue(regexp.match_ip_address("192.0.2.235"))
        self.assertTrue(regexp.match_ip_address("99.198.122.146"))
        self.assertTrue(regexp.match_ip_address("18.101.25.153"))
        self.assertTrue(regexp.match_ip_address("23.71.254.72"))
        self.assertTrue(regexp.match_ip_address("100.100.100.100"))
        self.assertTrue(regexp.match_ip_address("173.194.34.134"))
        self.assertTrue(regexp.match_ip_address("212.58.241.131"))
        self.assertTrue(regexp.match_ip_address("46.51.197.88"))
        self.assertFalse(regexp.match_ip_address("256.256.256.256"))
        self.assertFalse(regexp.match_ip_address("100.100.100"))
        self.assertFalse(regexp.match_ip_address(".100.100.100.100"))
        self.assertFalse(regexp.match_ip_address("100..100.100.100."))
        self.assertFalse(regexp.match_ip_address("100.100.100.100."))
        self.assertFalse(regexp.match_ip_address("256.100.100.100.100"))
        self.assertFalse(regexp.match_ip_address("212..241.131"))

    def test_match_date(self):
        self.assertTrue(regexp.match_date("18/09/2012"))
        self.assertTrue(regexp.match_date("30/09/2001"))
        self.assertTrue(regexp.match_date("01/12/1995"))
        # self.assertTrue(regexp.match_date("01/07/1001"))
        self.assertTrue(regexp.match_date("20/10/2010"))
        self.assertTrue(regexp.match_date("01/01/2000"))
        self.assertTrue(regexp.match_date("22/07/2007"))
        self.assertTrue(regexp.match_date("05/05/2010"))
        self.assertTrue(regexp.match_date("31/01/2011"))
        self.assertFalse(regexp.match_date("18/9/2002"))
        self.assertFalse(regexp.match_date("09-09.2023"))
        self.assertFalse(regexp.match_date("01.12.1995"))
        self.assertFalse(regexp.match_date("00/01/2012"))
        self.assertFalse(regexp.match_date("01/00/2012"))
        self.assertFalse(regexp.match_date("01/01/0000"))
        self.assertFalse(regexp.match_date("13/25/2012"))
        self.assertFalse(regexp.match_date("02/30/2012"))
        self.assertFalse(regexp.match_date("04/31/2012"))
        self.assertFalse(regexp.match_date("a11-11-2011"))
        self.assertFalse(regexp.match_date("05-05-2005d"))



    def test_get_dashes_words(self):
        self.assertEqual(regexp.get_dashes_words("Example bumble-gumble string"),
                         ('bumble', 'gumble'))
        self.assertEqual(regexp.get_dashes_words(
            "The first recorded versions of the rhyme date from late eighteenth-century England and the tune from 1870"),
                         ('eighteenth', 'century'))
        self.assertEqual(regexp.get_dashes_words("one of the best known in the English-speaking world"),
                         ('English', 'speaking'))


    def test_parse_http_url(self):
        self.assertEqual(regexp.parse_http_url("http://ya.ru"),
                         ("http", "ya.ru", 80, "/", ""))
        self.assertEqual(regexp.parse_http_url("http://www.example.org/"),
                         ("http", "www.example.org", 80, "/", ""))
        self.assertEqual(regexp.parse_http_url("http://bla.bla.biz"),
                         ("http", "bla.bla.biz", 80, "/", ""))
        self.assertEqual(regexp.parse_http_url("https://boring.museum"),
                         ("https", "boring.museum", 80, "/", ""))
        self.assertEqual(regexp.parse_http_url("http://0test.com/"),
                         ("http", "0test.com", 80, "/", ""))
        self.assertEqual(regexp.parse_http_url("http://this-test.com"),
                         ("http", "this-test.com", 80, "/", ""))
        self.assertEqual(regexp.parse_http_url("http://test.this-test.com/"),
                         ("http", "test.this-test.com", 80, "/", ""))
        self.assertEqual(regexp.parse_http_url("http://TESTdomain.com"),
                         ("http", "TESTdomain.com", 80, "/", ""))
        self.assertEqual(regexp.parse_http_url("invalid://example.com"),
                         None)
        self.assertEqual(regexp.parse_http_url("ihttp://example.com"),
                         None)
        self.assertEqual(regexp.parse_http_url("http://test ing.com"),
                         None)
        self.assertEqual(regexp.parse_http_url("http://test'ing.com"),
                         None)
        self.assertEqual(regexp.parse_http_url("http://test_ing.com"),
                         None)
        self.assertEqual(regexp.parse_http_url("http://"),
                         None)
        self.assertEqual(regexp.parse_http_url("http://.com"),
                         None)
        self.assertEqual(regexp.parse_http_url("http://example..com"),
                         None)
        self.assertEqual(regexp.parse_http_url("http://example.com."),
                         None)
        self.assertEqual(regexp.parse_http_url("http://-example.com"),
                         None)
        self.assertEqual(regexp.parse_http_url("http://example-.com"),
                         None)
        self.assertEqual(regexp.parse_http_url("http://example.com-"),
                         None)
        self.assertEqual(regexp.parse_http_url("https://TESTdomain.com:8080/path/to/method?asd=qwe"),
                         ("https", "TESTdomain.com", 8080, "/path/to/method", "asd=qwe"))
        self.assertEqual(regexp.parse_http_url("https://TESTdomain.com:1000000/path/to/method?asd=qwe"),
                         None)
        self.assertEqual(regexp.parse_http_url("https://TESTdomain.com:8080/path/to/method?asd=qwe#5543"),
                         ("https", "TESTdomain.com", 8080, "/path/to/method", "asd=qwe"))
        # uncomment in case of fire
        """
        self.assertEqual(regexp.parse_http_url("https://TESTdomain.com:8080/path//to/method?asd=qwe"),
                         None)
        self.assertEqual(regexp.parse_http_url("https://TESTdomain.com:8080/path/to/method?asd=qwe&triple=123"),
                         ("https", "TESTdomain.com", 8080, "/path/to/method", "asd=qwe&triple=123"))
        self.assertEqual(regexp.parse_http_url("https://TESTdomain.com:8080/path/to/method?asd=qwe&&&"),
                         None)
        self.assertEqual(regexp.parse_http_url("https://TESTdomain.com:8080/path/to/method?asd=qwe&triple=123?"),
                         None)
         """


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRegularExpressions)
    unittest.TextTestRunner(verbosity=2).run(suite)





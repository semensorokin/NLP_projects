# -*- coding: utf-8 -*-
import re

"""
'.'
    (Dot.) In the default mode, this matches any character except a newline. If the DOTALL flag has been specified,
    this matches any character including a newline.
'^'
    (Caret.) Matches the start of the string, and in MULTILINE mode also matches immediately after each newline.
'$'
    Matches the end of the string or just before the newline at the end of the string, and in MULTILINE mode
    also matches before a newline. foo matches both ‘foo’ and ‘foobar’, while the regular expression foo$ matches only ‘foo’. More interestingly, searching for foo.$ in 'foo1\nfoo2\n' matches ‘foo2’ normally, but ‘foo1’ in MULTILINE mode; searching for a single $ in 'foo\n' will find two (empty) matches: one just before the newline, and one at the end of the string.
"""
# match string of three characters
def match_three_letters(text):
    expr = re.compile("^...$")
    return bool(expr.match(text))

"""
match string of three characters
with 'a' as firs and 'c' last
Ex.
abc -> yes
a3c -> yes
a!c -> yes
abb -> no
bbc -> no
abbc -> no
"""
def match_a_smth_b(text):
    return None



"""
'*'
    Causes the resulting RE to match 0 or more repetitions of the preceding RE, as many repetitions as are possible.
    ab* will match ‘a’, ‘ab’, or ‘a’ followed by any number of ‘b’s.
'+'
    Causes the resulting RE to match 1 or more repetitions of the preceding RE.
    ab+ will match ‘a’ followed by any non-zero number of ‘b’s; it will not match just ‘a’.
'?'
    Causes the resulting RE to match 0 or 1 repetitions of the preceding RE. ab? will match either ‘a’ or ‘ab’.
"""

"""
Match string
with 'a', any count of b (nonzero) and 'c'
Ex.
abc -> yes
abbc -> yes
abbbbbc -> yes
abbbbb -> no
affc -> no
ac -> no
"""
def match_long_seq(text):
    return None

"""
    Check, if the string has letters between a
    "abba" -> yes
    "aqwertya" -> yes
    "aa" -> no
    "bba" -> no
    """
def match_letters_between(text):
    return None

"""
Check, if filename of MS Word 2013
qwerty.doc -> yes
qwerty.txt -> no
.doc -> yes
qwerty.docx -> no
"""
def match_doc_file(text):
    return None

"""
Check, if filename of MS Word 2016 or less version
qwerty.doc -> yes
qwerty.docx -> yes
.docx -> yes
qwerty.txt -> no
"""
def match_docx_file(text):
    return None



"""
Check, if filename of MS Word 2016 or less version
qwerty.doc -> yes
qwerty.docx -> yes
qwerty.txt -> no
.docx -> no
"""
def match_nonempty_docx_file(text):
    return None





"""
(...)
    Matches whatever regular expression is inside the parentheses, and indicates the start and end of a group;
    the contents of a group can be retrieved after a match has been performed, and can be matched later in the string
    with the number special sequence, described below. To match the literals '(' or ')', use \( or \), or enclose them
    inside a character class: [(] [)].
"""


"""
Find words with dash separator ('-')
Ex.

"Example bumble-gumble string" -> ('bumble','gumble')
"""

def get_dashes_words(text):
    return None



"""
'|'
    A|B, where A and B can be arbitrary REs, creates a regular expression that will match either A or B.
    An arbitrary number of REs can be separated by the '|' in this way.
    This can be used inside groups (see below) as well. As the target string is scanned, REs separated by '|' are tried
    from left to right. When one pattern completely matches, that branch is accepted.
    This means that once A matches, B will not be tested further, even if it would produce a longer overall match.
     In other words, the '|' operator is never greedy. To match a literal '|', use \|, or enclose it inside a character
     class, as in [|].
"""

"""
Found out, if the string is name Pavel Sukhov from capital letter or small letter

Pavel Sukhov -> yes
Pavel sukhov -> yes
Pavel sUkhov -> no
Anton Smirnov -> no
"""
def match_pavel_sukhov(text):
    return None

"""
{m}
    Specifies that exactly m copies of the previous RE should be matched; fewer matches cause
    the entire RE not to match. For example, a{6} will match exactly six 'a' characters, but not five.
{m,n}
    Causes the resulting RE to match from m to n repetitions of the preceding RE, attempting to match as
    many repetitions as possible. For example, a{3,5} will match from 3 to 5 'a' characters.
    Omitting m specifies a lower bound of zero, and omitting n specifies an infinite upper bound. As an example, a{4,}b
    will match aaaab or a thousand 'a' characters followed by a b, but not aaab.
    The comma may not be omitted or the modifier would be confused with the previously described form.
{m,n}?
    Causes the resulting RE to match from m to n repetitions of the preceding RE,
    attempting to match as few repetitions as possible. This is the non-greedy version of the
    previous qualifier. For example, on the 6-character string 'aaaaaa', a{3,5} will match 5 'a'
    characters, while a{3,5}? will only match 3 characters.
"""

"""
    Check, if the string has  2-4 "name"
    "lala name name lala name" -> yes
    "name this string is about name" -> yes
    "qwerty name" -> no
    """
def match_find_many_names(text):
    return None

"""
[]

    Used to indicate a set of characters. In a set:

        Characters can be listed individually, e.g. [amk] will match 'a', 'm', or 'k'.
        Ranges of characters can be indicated by giving two characters and separating them by a '-',
            for example [a-z] will match any lowercase ASCII letter, [0-5][0-9] will match all the
            two-digits numbers from 00 to 59, and [0-9A-Fa-f] will match any hexadecimal digit. If - is escaped
            (e.g. [a\-z]) or if it’s placed as the first or last character (e.g. [a-]), it will match a literal '-'.
        Special characters lose their special meaning inside sets. For example, [(+*)] will match any of the literal
            characters '(', '+', '*', or ')'.
        Character classes such as \w or \S (defined below) are also accepted inside a set, although the characters
            they match depends on whether LOCALE or UNICODE mode is in force.
        Characters that are not within a range can be matched by complementing the set. If the first character
            of the set is '^', all the characters that are not in the set will be matched.
            For example, [^5] will match any character except '5', and [^^] will match any character except '^'.
            ^ has no special meaning if it’s not the first character in the set.
        To match a literal ']' inside a set, precede it with a backslash, or place it at the beginning of the set.
            For example, both [()[\]{}] and []()[{}] will both match a parenthesis.
"""

"""
match vowels

Ex.
aoe -> Yes
iouye -> Yes
zoo -> No
aplw -> No
123a -> No

"""
def match_vowels(text):
    return None

"""
match no vowels

Ex.
swd -> Yes
1b -> Yes
sad -> No
1a -> No
123a -> No

"""
def match_no_vowels(text):
    return None



#####################
# # REAL PROBLEMS # #
#####################


"""
Match letters in alphabet order

axz -> yes
azx -> no

"""
def match_alphabet_order(text):
    return None





"""
Match ip address

192.0.2.235 -> yes
192.256.2.235 -> no

"""
def match_ip_address(text):
    return None

"""
Match date with format
DD/MM/YYYY

2012/09/18 -> Yes
2020/09/09 -> No
2020.09.09 -> No
2020/02/31 -> No  (31 February ?!)
"""
def match_date(text):
    return None


"""
Parse http url


                      port(optional)
   scheme             default: 80     method
     ||                   ||            ||          query(optional)
     \/                   \/            \/   ╔═════════════════════╗
    http://some.host.com:8080/path/to/method?param1=30&param2=qwerty#5589
               /\            ╚═════════════╝                          /\
               ||          path (may be just "/")                     ||
              host                                             Fragment(optional)



return (scheme, host, port, path, query)
return None if no much url
"""
def parse_http_url(text):
    return None


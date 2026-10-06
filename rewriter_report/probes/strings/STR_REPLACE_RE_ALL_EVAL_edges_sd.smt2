; replace_re_all differential: non-empty shortest matches, epsilon-accepting regex
; EXPECT: sat
(set-logic ALL)
(declare-const a String)(declare-const b String)(declare-const c String)(assert (= a (str.replace_re_all "abc" (re.* (str.to_re "x")) "-")))(assert (= b (str.replace_re_all "aaa" (re.+ (str.to_re "a")) "-")))(assert (= c (str.replace_re_all "abab" (re.union (str.to_re "ab") (str.to_re "b")) "-")))(assert (and (= a "abc") (= b "---") (= c "--")))
(check-sat)

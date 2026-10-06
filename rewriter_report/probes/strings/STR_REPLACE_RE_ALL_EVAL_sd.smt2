; replace_re_all: only non-empty matches, shortest leftmost
; EXPECT: sat
(set-logic ALL)
(assert (= (str.replace_re_all "abc" (re.* (str.to_re "x")) "-") "abc"))(assert (= (str.replace_re_all "aaa" (re.+ (str.to_re "a")) "-") "---"))(assert (= (str.replace_re_all "abab" (re.union (str.to_re "ab") (str.to_re "b")) "-") "--"))
(check-sat)

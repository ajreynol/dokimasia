; replace_re differential: empty match at 0, shortest leftmost match
; EXPECT: sat
(set-logic ALL)
(declare-const a String)(declare-const b String)(assert (= a (str.replace_re "abc" (re.* (str.to_re "x")) "-")))(assert (= b (str.replace_re "abab" (re.++ (str.to_re "a") (re.* re.allchar)) "-")))(assert (and (= a "-abc") (= b "-bab")))
(check-sat)

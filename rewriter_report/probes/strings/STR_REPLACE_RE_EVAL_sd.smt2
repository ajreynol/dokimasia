; replace_re: shortest leftmost match, empty match at 0
; EXPECT: sat
(set-logic ALL)
(assert (= (str.replace_re "abc" (re.* (str.to_re "x")) "-") "-abc"))(assert (= (str.replace_re "abab" (re.++ (str.to_re "a") (re.* re.allchar)) "-") "-bab"))(assert (= (str.replace_re "abc" re.none "-") "abc"))
(check-sat)

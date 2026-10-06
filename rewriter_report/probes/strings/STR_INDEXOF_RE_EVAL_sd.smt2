; indexof_re edge cases: start > len, start = len with epsilon, negative start, none
; EXPECT: sat
(set-logic ALL)
(assert (= (str.indexof_re "abc" (str.to_re "") 3) 3))(assert (= (str.indexof_re "abc" (str.to_re "") 4) (- 1)))(assert (= (str.indexof_re "abc" (str.to_re "c") (- 1)) (- 1)))(assert (= (str.indexof_re "abc" re.none 0) (- 1)))(assert (= (str.indexof_re "abcbc" (re.++ (str.to_re "b") (re.* re.allchar)) 2) 3))
(check-sat)

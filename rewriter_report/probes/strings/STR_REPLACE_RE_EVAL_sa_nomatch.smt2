; replace_re with no match returns s; empty s with non-nullable re
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (and (= (str.replace_re "abc" (str.to_re "d") "Q") "abc") (= (str.replace_re "" (str.to_re "a") "Q") "") (= (str.replace_re "" (re.* (str.to_re "a")) "Q") "Q"))))
(check-sat)

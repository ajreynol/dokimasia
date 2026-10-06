; re.loop 1 3 of a union eliminated to union of r, r^2, r^3
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.in_re x ((_ re.loop 1 3) (re.union (str.to_re "a") (str.to_re "bc")))) (str.in_re x (re.union (re.union (str.to_re "a") (str.to_re "bc")) (re.++ (re.union (str.to_re "a") (str.to_re "bc")) (re.union (str.to_re "a") (str.to_re "bc"))) (re.++ (re.union (str.to_re "a") (str.to_re "bc")) (re.union (str.to_re "a") (str.to_re "bc")) (re.union (str.to_re "a") (str.to_re "bc"))))))))
(check-sat)

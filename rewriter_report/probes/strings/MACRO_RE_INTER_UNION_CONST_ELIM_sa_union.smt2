; union (ab) | [a-b]*: constant included, dropped
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.in_re x (re.union (str.to_re "ab") (re.* (re.range "a" "b")))) (str.in_re x (re.* (re.range "a" "b"))))))
(check-sat)

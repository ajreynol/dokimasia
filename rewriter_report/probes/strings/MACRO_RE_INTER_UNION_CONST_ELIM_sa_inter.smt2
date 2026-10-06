; inter (ab) & [a-b]*: becomes (ab)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.in_re x (re.inter (str.to_re "ab") (re.* (re.range "a" "b")))) (= x "ab"))))
(check-sat)

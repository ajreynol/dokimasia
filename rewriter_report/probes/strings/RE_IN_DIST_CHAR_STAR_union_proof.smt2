; concat in star of union of char REs distributes
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re (str.++ x y) (re.* (re.union (str.to_re "a") (re.range "x" "z")))) (and (str.in_re x (re.* (re.union (str.to_re "a") (re.range "x" "z")))) (str.in_re y (re.* (re.union (str.to_re "a") (re.range "x" "z"))))))))
(check-sat)

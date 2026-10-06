; union of two consts both in R collapses to R
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.in_re x (re.union (str.to_re "ab") (str.to_re "ba") (re.* (re.range "a" "b")))) (str.in_re x (re.* (re.range "a" "b"))))))
(check-sat)

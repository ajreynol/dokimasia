; union flattening, dedup, drop re.none
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.union (re.union (str.to_re "a") (str.to_re "b")) re.none (str.to_re "a"))) (str.in_re x (re.union (str.to_re "a") (str.to_re "b"))))))
(check-sat)

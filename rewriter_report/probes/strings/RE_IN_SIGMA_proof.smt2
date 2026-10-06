; x in allchar iff len x = 1
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x re.allchar) (= (str.len x) 1))))
(check-sat)

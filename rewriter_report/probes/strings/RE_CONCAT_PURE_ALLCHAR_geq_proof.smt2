; x in _ _* _ iff len x >= 2
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (re.++ re.allchar (re.* re.allchar) re.allchar)) (>= (str.len x) 2))))
(check-sat)

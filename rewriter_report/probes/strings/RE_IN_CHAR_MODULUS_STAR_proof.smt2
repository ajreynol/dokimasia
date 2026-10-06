; x in (allchar^3)* iff len x mod 3 = 0
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (re.* (re.++ re.allchar re.allchar re.allchar))) (= (mod (str.len x) 3) 0))))
(check-sat)

; x in _ _ _ iff len x = 3
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.in_re x (re.++ re.allchar re.allchar re.allchar)) (= (str.len x) 3))))
(check-sat)

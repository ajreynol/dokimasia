; x in (_ _ _)* iff len x mod 3 = 0
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.in_re x (re.* (re.++ re.allchar re.allchar re.allchar))) (= (mod (str.len x) 3) 0))))
(check-sat)

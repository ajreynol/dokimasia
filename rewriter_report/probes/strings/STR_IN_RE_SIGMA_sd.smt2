; x in __ = len x = 2 ; x in _ _* _ = len x >= 2
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (or (not (= (str.in_re x (re.++ re.allchar re.allchar)) (= (str.len x) 2))) (not (= (str.in_re x (re.++ re.allchar (re.* re.allchar) re.allchar)) (>= (str.len x) 2)))))
(check-sat)

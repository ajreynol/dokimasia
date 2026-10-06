; len(x)+len(y)+1 = len(x) is false (rewritePredViaEntailment on EQUAL)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (= (+ (str.len x) (str.len y) 1) (str.len x)))
(check-sat)

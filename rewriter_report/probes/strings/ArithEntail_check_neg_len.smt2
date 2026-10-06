; substr with length -len(y)-1 is empty
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr x n (- (- 1) (str.len y))) "")))
(check-sat)

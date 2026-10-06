; substr with start -1-len(y) is empty (strict negativity)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr x (- (- 1) (str.len y)) n) "")))
(check-sat)

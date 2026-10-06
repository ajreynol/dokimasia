; str.to_int(x) >= -1
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (< (+ (str.to_int x) (str.len y)) (- 1)))
(check-sat)

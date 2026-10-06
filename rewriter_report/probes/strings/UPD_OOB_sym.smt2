; update at index entailed >= len
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.update x (+ (str.len x) (str.len y)) z) x)))
(check-sat)

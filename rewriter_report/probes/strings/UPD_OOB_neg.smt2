; update at index entailed < 0
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.update x (- (- 1) (str.len y)) z) x)))
(check-sat)

; update of reverse at out of range index
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.update (str.rev x) (+ (str.len x) n) "a") (str.rev x))))
(assert (>= n 0))
(check-sat)

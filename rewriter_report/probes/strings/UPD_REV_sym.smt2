; update of reverse with single char
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.update (str.rev x) n "a") (str.rev (str.update x (- (str.len x) (+ n 1)) "a")))))
(check-sat)

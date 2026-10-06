; update of reverse with len<=1 symbolic replacement
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.update (str.rev x) n (str.substr y 0 1)) (str.rev (str.update x (- (str.len x) (+ n 1)) (str.substr y 0 1))))))
(check-sat)

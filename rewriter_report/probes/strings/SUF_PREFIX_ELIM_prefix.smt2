; prefixof elim
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.prefixof x y) (= x (str.substr y 0 (str.len x))))))
(check-sat)

; suffixof elim
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.suffixof x y) (= x (str.substr y (- (str.len y) (str.len x)) (str.len x))))))
(check-sat)

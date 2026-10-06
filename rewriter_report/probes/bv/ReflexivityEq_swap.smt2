; ReflexivityEq: (= y x) and (= x y) are normalized to one orientation (node-id order).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(declare-const y (_ BitVec 3))
(declare-const p Bool)
(assert (= p (= x y)))
(assert (not (= p (= y x))))
(check-sat)

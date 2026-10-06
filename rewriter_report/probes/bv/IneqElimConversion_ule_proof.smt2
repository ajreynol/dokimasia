; Proof probe: (bvule c (int2bv 3 i)) with constant on the left -> (<= c (mod i 8)) (IneqElimConversion, ULE branch).
; EXPECT: unsat
(set-logic ALL)
(declare-const i Int)
(assert (bvule #b110 ((_ int2bv 3) i)))
(assert (< (mod i 8) 6))
(check-sat)

; XorSimplify corner case: (bvxor (bvnot a) a) = ones, handled by the elaborator's appended-#b0000 path.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 4))
(assert (not (= (bvxor (bvnot a) a) #b1111)))
(check-sat)

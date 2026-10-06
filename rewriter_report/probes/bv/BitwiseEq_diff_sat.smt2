; BitwiseEq differential: (bvor a b)=#b0 with (bvnot a)=#b1 sat; nor/nand eliminated earlier
; EXPECT: sat
; CVC5-OPTS: --bitwise-eq
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (= (bvor x y) #b0))
(assert (= (bvnot x) #b1))
(assert (= (bvcomp x y) #b1))
(check-sat)

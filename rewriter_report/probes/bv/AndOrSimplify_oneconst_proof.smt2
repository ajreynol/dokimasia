; AndSimplify/OrSimplify: single constant with duplicates and nested negation in pre-rewrite (consts<=1 path, RARE/ACI only)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (or (not (= (bvand (bvnot x) y #b1111 (bvnot x)) (bvand y (bvnot x)))) (not (= (bvor (bvnot x) y #b0000 y) (bvor y (bvnot x))))))
(check-sat)

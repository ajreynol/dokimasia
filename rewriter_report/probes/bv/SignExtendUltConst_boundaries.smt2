; Differential: every constant c at n=2,m=2 on both sides, checked against z3 via exhaustive equality with a reference encoding (bvslt-free).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 2))
(define-fun S () (_ BitVec 4) ((_ sign_extend 2) x))
(define-fun R () (_ BitVec 4) (concat (ite (= ((_ extract 1 1) x) #b1) #b11 #b00) x))
(assert (or
 (not (= (bvult S #x0) (bvult R #x0))) (not (= (bvult S #x1) (bvult R #x1))) (not (= (bvult S #x2) (bvult R #x2))) (not (= (bvult S #x3) (bvult R #x3)))
 (not (= (bvult S #x4) (bvult R #x4))) (not (= (bvult S #x5) (bvult R #x5))) (not (= (bvult S #x6) (bvult R #x6))) (not (= (bvult S #x7) (bvult R #x7)))
 (not (= (bvult S #x8) (bvult R #x8))) (not (= (bvult S #x9) (bvult R #x9))) (not (= (bvult S #xa) (bvult R #xa))) (not (= (bvult S #xb) (bvult R #xb)))
 (not (= (bvult S #xc) (bvult R #xc))) (not (= (bvult S #xd) (bvult R #xd))) (not (= (bvult S #xe) (bvult R #xe))) (not (= (bvult S #xf) (bvult R #xf)))
 (not (= (bvult #x0 S) (bvult #x0 R))) (not (= (bvult #x1 S) (bvult #x1 R))) (not (= (bvult #x2 S) (bvult #x2 R))) (not (= (bvult #x3 S) (bvult #x3 R)))
 (not (= (bvult #x4 S) (bvult #x4 R))) (not (= (bvult #x5 S) (bvult #x5 R))) (not (= (bvult #x6 S) (bvult #x6 R))) (not (= (bvult #x7 S) (bvult #x7 R)))
 (not (= (bvult #x8 S) (bvult #x8 R))) (not (= (bvult #x9 S) (bvult #x9 R))) (not (= (bvult #xa S) (bvult #xa R))) (not (= (bvult #xb S) (bvult #xb R)))
 (not (= (bvult #xc S) (bvult #xc R))) (not (= (bvult #xd S) (bvult #xd R))) (not (= (bvult #xe S) (bvult #xe R))) (not (= (bvult #xf S) (bvult #xf R)))))
(check-sat)

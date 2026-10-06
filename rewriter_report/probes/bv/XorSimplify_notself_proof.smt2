; XorSimplify corner (issue 12336): x ^ ~x -> ones, no constant child
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (= #b0001 (bvxor x (bvnot x))))
(check-sat)

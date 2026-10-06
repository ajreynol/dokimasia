; FlattenAssocCommut: nested bvadd/bvmul/bvand flattened (BV_POLY_NORM / ACI_NORM)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (or (not (= (bvadd x (bvadd y (bvadd z x))) (bvadd (bvmul x #b0010) y z))) (not (= (bvmul x (bvmul y z)) (bvmul z y x))) (not (= (bvxor x (bvxor y z)) (bvxor z y x)))))
(check-sat)

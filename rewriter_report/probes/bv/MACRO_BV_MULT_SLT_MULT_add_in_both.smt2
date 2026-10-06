; Sound sext/sext MultSltMult where the shared factor a is itself a bvadd; the elaborator swaps the wrong mult and leaves a trusted residue.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const p (_ BitVec 4))
(declare-const q (_ BitVec 4))
(declare-const x (_ BitVec 4))
(declare-const t (_ BitVec 4))
(assert (not (= (bvslt (bvmul ((_ sign_extend 4) (bvadd p q)) ((_ sign_extend 4) (bvadd x t)))
                       (bvmul ((_ sign_extend 4) (bvadd x t)) ((_ sign_extend 4) p)))
                (and (not (= q #x0)) (not (= (bvadd x t) #x0))
                     (= (bvslt (bvadd p q) p) (bvsgt (bvadd x t) #x0))))))
(check-sat)

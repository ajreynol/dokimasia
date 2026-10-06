; ExtractSignExtend differential: case2 boundary keeps sign semantics (bit4=bit3=1, bit2=0 is sat)
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (= ((_ extract 4 2) ((_ sign_extend 2) x)) #b110))
(check-sat)

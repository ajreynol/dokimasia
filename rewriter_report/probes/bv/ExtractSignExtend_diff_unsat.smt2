; ExtractSignExtend differential: bits above n must equal sign bit (case3 unsat)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= ((_ extract 5 4) ((_ sign_extend 2) x)) (ite (= ((_ extract 3 3) x) #b1) #b11 #b00))))
(check-sat)

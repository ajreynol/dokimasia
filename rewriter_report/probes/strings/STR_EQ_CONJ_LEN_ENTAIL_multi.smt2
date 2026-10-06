; x = y++x++z <=> y="" and z=""
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= x (str.++ y x z)) (and (= y "") (= z "")))))
(check-sat)

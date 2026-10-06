; x = y++x++z iff y="" and z=""
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (= x (str.++ y x z)) (and (= y "") (= z "")))))
(check-sat)

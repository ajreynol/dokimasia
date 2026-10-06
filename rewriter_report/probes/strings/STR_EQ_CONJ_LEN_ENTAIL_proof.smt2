; x++a = a++x++z <=> x++a = a++x and z = ""
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ x "a") (str.++ "a" x z)) (and (= (str.++ x "a") (str.++ "a" x)) (= z "")))))
(check-sat)

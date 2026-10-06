; flipped orientation: a++x++z = x++a <=> x++a = a++x and z = ""
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ "a" x z) (str.++ x "a")) (and (= (str.++ x "a") (str.++ "a" x)) (= z "")))))
(check-sat)

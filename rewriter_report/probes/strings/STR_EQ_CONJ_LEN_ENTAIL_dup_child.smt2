; w++a = z++a++w++z <=> w++a = a++w and z = "" (duplicate concat child z)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ w "a") (str.++ z "a" w z)) (and (= (str.++ w "a") (str.++ "a" w)) (= z "")))))
(check-sat)

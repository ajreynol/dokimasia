; str.at(w,n)++x = z++a++x++u: lhs length <=1+len x
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const u String)
(declare-const n Int)
(assert (not (= (= (str.++ (str.at w n) x) (str.++ z "a" x u)) (and (= (str.++ (str.at w n) x) (str.++ "a" x)) (= z "") (= u "")))))
(check-sat)

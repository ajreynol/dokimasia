; x++y in (str.to_re x++y) consumes symbolically
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.in_re (str.++ x y z) (re.++ (str.to_re (str.++ x y)) (re.* re.allchar))) true)))
(check-sat)

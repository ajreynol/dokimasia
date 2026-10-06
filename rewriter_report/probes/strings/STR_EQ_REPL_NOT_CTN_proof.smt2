; x = replace(x,a,b) <=> not contains(x,a)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= x (str.replace x "a" "b")) (not (str.contains x "a")))))
(check-sat)

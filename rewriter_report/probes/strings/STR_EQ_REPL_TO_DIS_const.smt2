; replace(x,a,b) = b <=> x=a or x=b
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.replace x "a" "b") "b") (or (= x "a") (= x "b")))))
(check-sat)

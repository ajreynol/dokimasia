; str.at at negative/oob index is empty
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (= x "ab"))
(assert (or (not (= (str.at x (- 1)) "")) (not (= (str.at x 2) "")) (not (= (str.at x 1) "b"))))
(check-sat)

; str.at eliminated to substr len 1
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.at x 1) (str.substr x 1 1))))
(check-sat)

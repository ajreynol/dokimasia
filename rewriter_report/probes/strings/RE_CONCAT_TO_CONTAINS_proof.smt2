; x in _* y _* iff contains x y (symbolic y)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (re.++ (re.* re.allchar) (str.to_re y) (re.* re.allchar))) (str.contains x y))))
(check-sat)

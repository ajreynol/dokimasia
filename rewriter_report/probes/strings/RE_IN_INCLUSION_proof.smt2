; x++a++y in _* (a|b) _* is true by RE inclusion
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.in_re (str.++ x "a" y) (re.++ (re.* re.allchar) (re.union (str.to_re "a") (str.to_re "b")) (re.* re.allchar))) true)))
(check-sat)

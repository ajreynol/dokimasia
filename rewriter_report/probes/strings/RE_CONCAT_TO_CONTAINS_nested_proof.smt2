; x in _* (abc) _* _* normalizes then becomes contains
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (re.++ (re.* re.allchar) (str.to_re "ab") (re.* re.allchar) (re.* re.allchar))) (str.contains x "ab"))))
(check-sat)

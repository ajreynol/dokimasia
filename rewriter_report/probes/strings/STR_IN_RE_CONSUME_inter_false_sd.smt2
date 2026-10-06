; "ab"++x in inter(c.Sigma*, Sigma*) = false
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)
(assert (str.in_re (str.++ "ab" x) (re.inter (re.++ (str.to_re "c") (re.* re.allchar)) (re.* re.allchar))))
(check-sat)

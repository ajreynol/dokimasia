; "a"++x in a.Sigma* = true
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (str.in_re (str.++ "a" x) (re.++ (str.to_re "a") (re.* re.allchar)))))
(check-sat)

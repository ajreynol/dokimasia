; "ac"++x in a.b.Sigma* = false
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (str.in_re (str.++ "ac" x) (re.++ (str.to_re "a") (str.to_re "b") (re.* re.allchar))))
(check-sat)

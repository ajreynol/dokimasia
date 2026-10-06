; "\u{2ffff}"++x in [\u{0}-\u{2ffff}].Sigma*; and "b"++x in [c-d].Sigma* false
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)
(assert (or (not (str.in_re (str.++ "\u{2ffff}" x) (re.++ (re.range "\u{0}" "\u{2ffff}") (re.* re.allchar)))) (str.in_re (str.++ "b" x) (re.++ (re.range "c" "d") (re.* re.allchar)))))
(check-sat)

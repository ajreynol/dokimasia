; x++\u{2ffff} in .*[\u{2fffe}-\u{2ffff}] is valid
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (str.in_re (str.++ x "\u{2ffff}") (re.++ (re.* re.allchar) (re.range "\u{2fffe}" "\u{2ffff}")))))
(check-sat)

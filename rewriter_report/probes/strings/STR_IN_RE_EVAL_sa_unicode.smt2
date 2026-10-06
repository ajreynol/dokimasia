; membership of max code point in full range is true; just beyond a smaller range is false
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (or (not (str.in_re "\u{2ffff}" (re.range "\u{0}" "\u{2ffff}"))) (str.in_re "\u{100}" (re.range "\u{0}" "\u{ff}"))))
(check-sat)

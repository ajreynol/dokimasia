; \u{2ffff}++x = \u{2fffe}++y: clash at max code points
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ "\u{2ffff}" x) (str.++ "\u{2fffe}" y)) false)))
(check-sat)

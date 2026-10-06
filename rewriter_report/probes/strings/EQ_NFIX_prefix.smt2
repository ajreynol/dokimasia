; ab++x = ac++y: prefix clash
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ "ab" x) (str.++ "ac" y)) false)))
(check-sat)

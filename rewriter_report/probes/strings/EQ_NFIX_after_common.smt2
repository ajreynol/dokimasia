; z++ab++x = z++ac++y: clash after common component
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ z "ab" x) (str.++ z "ac" y)) false)))
(check-sat)

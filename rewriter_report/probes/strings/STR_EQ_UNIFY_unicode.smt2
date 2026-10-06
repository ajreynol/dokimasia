; \u{10000}a++x = \u{10000}++y <=> a++x = y
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ "\u{10000}a" x) (str.++ "\u{10000}" y)) (= (str.++ "a" x) y))))
(check-sat)

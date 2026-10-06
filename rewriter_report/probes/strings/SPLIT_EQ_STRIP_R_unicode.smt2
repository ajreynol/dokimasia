; \u{10000}++x++y = x++\u{10000}\u{5c}++z <=> ... (unicode strip)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ "\u{10000}" x y) (str.++ x "\u{10000}\u{5c}" z)) (and (= (str.++ "\u{10000}" x) (str.++ x "\u{10000}")) (= y (str.++ "\u{5c}" z))))))
(check-sat)

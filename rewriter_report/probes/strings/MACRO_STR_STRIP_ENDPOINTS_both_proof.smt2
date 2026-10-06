; contains strips both endpoints
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.contains (str.++ "ab" x "cd") (str.++ "b" y "c")) (str.contains (str.++ "b" x "c") (str.++ "b" y "c")))))
(check-sat)

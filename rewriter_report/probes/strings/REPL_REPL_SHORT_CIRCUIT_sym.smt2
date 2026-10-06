; lookahead short circuit with constants
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.replace x "ab" x) x "c") (str.replace (str.replace x "ab" "c") x "c"))))
(check-sat)

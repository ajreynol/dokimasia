; len(replace(x,ab,cd)) = len x
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const u String)
(assert (not (= (str.len (str.replace x "ab" "cd")) (str.len x))))
(check-sat)

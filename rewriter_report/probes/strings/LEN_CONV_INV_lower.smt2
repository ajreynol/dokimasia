; len(to_lower x) = len x
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const u String)
(assert (not (= (str.len (str.to_lower x)) (str.len x))))
(check-sat)

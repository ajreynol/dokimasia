; indexof_re evaluation
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof_re "xaab" (re.+ (str.to_re "a")) 0) 1)))
(check-sat)

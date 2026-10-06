; indexof_re negative start
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof_re x (str.to_re "a") (- 1)) (- 1))))
(check-sat)

; indexof_re nullable regex at start == len
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof_re x (re.* (str.to_re "a")) (str.len x)) (str.len x))))
(check-sat)

; indexof_re with start > len
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.indexof_re x re.all (+ 1 (str.len x))) (- 1))))
(check-sat)

; proof of indexof_re evaluation
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (= x "abcbc"))(assert (not (= (str.indexof_re x (str.to_re "c") 3) 4)))
(check-sat)

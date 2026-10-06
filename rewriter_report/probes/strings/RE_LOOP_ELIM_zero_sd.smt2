; loop 0 0 is epsilon; loop 2 1 is none
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (or (not (= (str.in_re x ((_ re.loop 0 0) (str.to_re "a"))) (= x ""))) (str.in_re x ((_ re.loop 2 1) (str.to_re "a")))))
(check-sat)

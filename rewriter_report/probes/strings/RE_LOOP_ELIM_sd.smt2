; x in (loop 1 3 a) iff x in {a,aa,aaa}
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.in_re x ((_ re.loop 1 3) (str.to_re "a"))) (or (= x "a") (= x "aa") (= x "aaa")))))
(check-sat)

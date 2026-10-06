; x++y = to_upper(x)++z iff x=to_upper(x) and y=z
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (= (str.++ x y) (str.++ (str.to_upper x) z)) (and (= x (str.to_upper x)) (= y z)))))
(check-sat)

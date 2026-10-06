; x++y = rev(x)++z iff x=rev(x) and y=z
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (= (str.++ x y) (str.++ (str.rev x) z)) (and (= x (str.rev x)) (= y z)))))
(check-sat)

; len(x)+len(z) >= len(replace(x,y,z)) via approximation
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (> (str.len (str.replace x y z)) (+ (str.len x) (str.len z))))
(check-sat)

; indexof(x,y,n) >= -1 and <= len(x)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (or (< (str.indexof x y n) (- 1)) (> (str.indexof x y n) (str.len x))))
(check-sat)

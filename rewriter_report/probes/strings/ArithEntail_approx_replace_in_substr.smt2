; substr start len(replace(x,y,z))+len y >= len x via replace under-approx -> empty
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr x (+ (str.len (str.replace x y z)) (str.len y)) n) "")))
(check-sat)

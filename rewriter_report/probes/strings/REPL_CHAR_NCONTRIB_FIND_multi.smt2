; replace char miniscope over two trailing components
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.++ x y x y) "A" z) (str.++ (str.replace (str.++ x y) "A" z) x y))))
(check-sat)

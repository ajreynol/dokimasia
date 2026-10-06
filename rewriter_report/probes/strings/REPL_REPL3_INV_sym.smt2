; replace x w (replace z x y) with z lacking w
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace x "c" (str.replace "ab" x y)) (str.replace x "c" "ab"))))
(check-sat)

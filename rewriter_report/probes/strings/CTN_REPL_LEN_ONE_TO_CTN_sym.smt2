; contains (replace x y x) z, len z <= 1
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.contains (str.replace x y x) (str.substr z 0 1)) (str.contains x (str.substr z 0 1)))))
(check-sat)

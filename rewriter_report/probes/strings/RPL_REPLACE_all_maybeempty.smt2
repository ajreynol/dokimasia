; replace_all x x y not rewritten when x may be empty
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace_all x x y) y)))
(check-sat)

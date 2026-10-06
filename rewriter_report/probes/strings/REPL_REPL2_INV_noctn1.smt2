; replace x (replace y x z) y with y lacking z
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace x (str.replace "ab" x "c") "ab") (str.replace x "ab" "ab"))))
(check-sat)

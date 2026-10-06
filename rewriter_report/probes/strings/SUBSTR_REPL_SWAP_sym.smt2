; substr prefix of replace with single chars
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.substr (str.replace x "a" "b") 0 n) (str.replace (str.substr x 0 n) "a" "b"))))
(check-sat)

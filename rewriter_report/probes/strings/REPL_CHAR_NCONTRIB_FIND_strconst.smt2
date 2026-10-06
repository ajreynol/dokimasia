; string: trailing var contained in prefix, char pattern
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace (str.++ x "b" (str.substr x 0 1)) "a" y) (str.++ (str.replace (str.++ x "b") "a" y) (str.substr x 0 1)))))
(check-sat)

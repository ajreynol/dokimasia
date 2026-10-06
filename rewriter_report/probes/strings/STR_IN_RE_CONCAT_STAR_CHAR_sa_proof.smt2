; x++y in [a-b]* iff x in [a-b]* and y in [a-b]*
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.in_re (str.++ x y) (re.* (re.range "a" "b"))) (and (str.in_re x (re.* (re.range "a" "b"))) (str.in_re y (re.* (re.range "a" "b")))))))
(check-sat)

; x++y in [a-c]* iff x in [a-c]* and y in [a-c]*
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.in_re (str.++ x y) (re.* (re.range "a" "c"))) (and (str.in_re x (re.* (re.range "a" "c"))) (str.in_re y (re.* (re.range "a" "c")))))))
(check-sat)

; "aaab"++x in a*.b.c* iff x in c* (consume through star)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.in_re (str.++ "aaab" x) (re.++ (re.* (str.to_re "a")) (str.to_re "b") (re.* (str.to_re "c")))) (str.in_re x (re.* (str.to_re "c"))))))
(check-sat)

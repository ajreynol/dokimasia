; x++"ba" in c*.b.a iff x in c*
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.in_re (str.++ x "ba") (re.++ (re.* (str.to_re "c")) (str.to_re "b") (str.to_re "a"))) (str.in_re x (re.* (str.to_re "c"))))))
(check-sat)

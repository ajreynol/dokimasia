; "abab"++x in (ab)*.c iff x in (ab)*.c ; star must unroll
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)
(assert (not (= (str.in_re (str.++ "abab" x) (re.++ (re.* (str.to_re "ab")) (str.to_re "c"))) (str.in_re x (re.++ (re.* (str.to_re "ab")) (str.to_re "c"))))))
(check-sat)

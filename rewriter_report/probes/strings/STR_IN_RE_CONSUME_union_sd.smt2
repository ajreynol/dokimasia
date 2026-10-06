; "ab"++x in (a.b | a.c).d* iff x in d* (union branches consume to same residual)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)
(assert (not (= (str.in_re (str.++ "ab" x) (re.++ (re.union (str.to_re "ab") (str.to_re "ac")) (re.* (str.to_re "d")))) (str.in_re x (re.* (str.to_re "d"))))))
(check-sat)

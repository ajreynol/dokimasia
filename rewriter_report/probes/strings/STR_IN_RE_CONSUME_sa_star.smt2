; consume through star body: ab++x in (ab)* iff x in (ab)*
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.in_re (str.++ "ab" x) (re.* (str.to_re "ab"))) (str.in_re x (re.* (str.to_re "ab"))))))
(check-sat)

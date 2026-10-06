; RE equality between distinct languages a* and a+ (differ on empty string) is false via RE_EQ_ELIM
; EXPECT: unsat
(set-logic ALL)
(assert (= (re.* (str.to_re "a")) (re.+ (str.to_re "a"))))
(check-sat)

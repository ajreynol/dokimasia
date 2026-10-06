; a* = a+ as regexes is false (empty word)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (= (re.* (str.to_re "a")) (re.+ (str.to_re "a"))))
(check-sat)

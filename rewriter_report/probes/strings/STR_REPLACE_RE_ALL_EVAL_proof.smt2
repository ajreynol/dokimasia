; replace_re_all on constants: non-empty shortest matches
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (and (= (str.replace_re_all "ZABCZAB" (re.++ (str.to_re "A") (re.* re.allchar) (str.to_re "C")) y) (str.++ "Z" y "ZAB")) (= (str.replace_re_all "aaa" (re.+ (str.to_re "a")) "b") "bbb") (= (str.replace_re_all "abc" (re.* (str.to_re "q")) "x") "abc") (= (str.replace_re_all "abab" (str.to_re "ab") "") ""))))
(check-sat)

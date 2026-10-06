; replace_re on constants: shortest leftmost match; empty match inserts at front
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (and (= (str.replace_re "ZABCZ" (re.++ (str.to_re "A") (re.* re.allchar) (str.to_re "C")) y) (str.++ "Z" y "Z")) (= (str.replace_re "abab" (re.+ (str.to_re "ab")) "x") "xab") (= (str.replace_re "abc" (re.* (str.to_re "q")) "x") "xabc") (= (str.replace_re "abc" (str.to_re "d") "x") "abc"))))
(check-sat)

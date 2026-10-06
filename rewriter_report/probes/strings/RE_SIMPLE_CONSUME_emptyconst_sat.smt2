; consume with empty string literal component; x=ab sat
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.in_re (str.++ x "" y) (re.++ (str.to_re "a") (re.* (str.to_re "b")))))
(assert (not (= x "")))
(assert (not (= y "")))
(check-sat)

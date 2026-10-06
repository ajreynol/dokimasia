; re.loop 0 2: union includes epsilon; aaa is not a member
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (str.in_re x ((_ re.loop 0 2) (str.to_re "a"))))
(assert (not (= x "")))
(assert (not (= x "a")))
(check-sat)

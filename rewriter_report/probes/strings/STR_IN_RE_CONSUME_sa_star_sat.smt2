; star consume must not be over-eager: ab++x in (ab|a)* with x=aab (abaab) is sat
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (str.in_re (str.++ "ab" x) (re.* (re.union (str.to_re "ab") (str.to_re "a")))))
(assert (= x "aab"))
(check-sat)

; "a"++x in (ab)*.a.y: x="" fits by skipping star
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)
(assert (str.in_re (str.++ "a" x) (re.++ (re.* (str.to_re "ab")) (str.to_re "a") (re.* (str.to_re "z")))))(assert (= x ""))
(check-sat)

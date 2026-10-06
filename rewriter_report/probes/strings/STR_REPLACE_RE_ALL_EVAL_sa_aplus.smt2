; replace_re_all shortest non-empty matches of a+ in aaba gives y y b y
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.replace_re_all "aaba" (re.+ (str.to_re "a")) y) (str.++ y y "b" y))))
(check-sat)

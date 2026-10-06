; merging \u{10000} with a, and escape boundary \u{5c} followed by u
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const u String)
(assert (not (= (str.++ x "\u{10000}" (str.++ "a" "\u{5c}" "u") y) (str.++ x "\u{10000}a\u{5c}u" y))))
(check-sat)

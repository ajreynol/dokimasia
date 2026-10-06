; to_lower/to_upper only touch ASCII letters (boundary chars @ [ ` { and non-ASCII)
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const a String)(declare-const b String)
(assert (= a (str.to_lower "@AZ[`az{\u{c9}")))(assert (= b (str.to_upper "@AZ[`az{\u{e9}")))
(assert (and (= a "@az[`az{\u{c9}") (= b "@AZ[`AZ{\u{e9}")))
(check-sat)

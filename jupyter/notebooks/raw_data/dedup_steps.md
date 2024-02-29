# remove std prefix
<CREATED VARIABLE> 
<RECODED VARIABLE> 
<SUMMARY VARIABLE> 

# dot notation (12A.3.)
^\d+[\D]\.(\d\.\D){1,}\s+

# dot notation with hyphens, 2 level dot notation
^\d\D\.\d\.\D.\s+

# non-greedy dot notation
^\d\D\.\d\.\D+\.\D+\.\s+
^\d\D\.\d\.\D+\.\D+\.\s+?
^\d\D\.\d\.\D+\.\D+\. ?
^\d\D\.\d\.(\D+){0,3}\.I{0,3}\.\s?
^\d\D\.\d\.\D+\.I{0,3}\.?
^\d\D\.\d\. ?

<!-- ^\d\D\.(\d\.\D\.){1,}?
^\d\D\.(\d\.\D){1,}\.\D+?\. -->
# roman numerals
# 11B.5.C.I.
^\d\D\.\d\.\D\.\D+.\
^\d\..\..\.I{0,3}\.
^\d\..\..\.I{0,3}

# leading numberletters
^\d+[\D]\. 
^"\d+[\D]\.

# leading number.letters
^\d+[\D]\. 
^"\d+[\D]\.

# leading letternumber
^\D\d+\.
^\D\d+ \- 
^\D\d+\s+\-


return to mg2.5 --> 2.5 GM
mg5.0 --> 5.0 GM
mg10 --> 10.0 GM
dim3 3d
HOUR48 48 HOUR
# final
^\D\d+?(\D){0,3}\.
^\d+?\.(\d+){0,3} 


^[:alpha:]\d+?[:alpha:]+?
"""
This module is the same as `canvaslms.grades.conjunctavg` except that any 
submissions with grades other than A--F and P/F are treated as P. For instance, 
numeric grades (like points). Also, all submissions must have a date. This 
makes this module useful for including mandatory, ungraded surveys.
"""

import datetime as dt
from canvaslms.grades.conjunctavg import a2e_average

def summarize(user, assignments_list):
  """
  Extracts user's submissions for assignments in assingments_list to summarize 
  results into one grade and a grade date. Summarize by conjunctive average.

  If some submission lacks date, return ("F", None).
  """

  pf_grades = []
  a2e_grades = []
  recent_date = dt.date(year=1970, month=1, day=1)

  for assignment in assignments_list:
    submission = assignment.get_submission(user)
    grade = submission.grade

    if grade is None:
      grade = "F"

    if grade in "ABCDE":
      a2e_grades.append(grade)
    elif grade in "PF":
      pf_grades.append(grade)
    else:
      pf_grades.append("E")

    grade_date = submission.submitted_at or submission.graded_at

    if not grade_date:
      return ("F", None)
    else:
      grade_date = dt.date.fromisoformat(grade_date.split("T")[0])

    if grade_date > recent_date:
      recent_date = grade_date

  if not all(map(lambda x: x == "P", pf_grades)):
    return ("F", recent_date)

  if a2e_grades:
    return (a2e_average(a2e_grades), recent_date)
  return ("P", recent_date)

def summarize_group(assignments_list, users_list):
  """Summarizes a particular set of assignments (assignments_list) for all
  users in users_list"""

  for user in users_list:
    grade, grade_date = summarize(user, assignments_list)
    yield (user, grade, grade_date)

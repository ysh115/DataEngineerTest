SELECT COUNT(*) AS 'Number of students have more than 2 subjects with score 85 or above'
FROM
(SELECT studentID, studentName, SUM([>=85]) AS 'number_of_subjects_over_85'
FROM
(SELECT student_marks.studentID, studentName, marks, (CASE WHEN marks >= 85 THEN 1 ELSE 0 END) AS '>=85' FROM
(SELECT studentID, [subject], marks FROM examResult ) AS student_marks
LEFT JOIN
student
ON
student_marks.studentID = student.studentID) AS student_marks
GROUP BY studentID, studentName
HAVING SUM([>=85]) > 2) AS student_summary
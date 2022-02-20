SELECT studentID, studentName, average_marks, rank() OVER(ORDER BY average_marks DESC) AS ranking
FROM
(SELECT DISTINCT studentID, studentName, average_marks
FROM
(SELECT student_average_marks.studentID AS studentID, studentName, [subject], marks, AVG(marks) OVER(PARTITION BY student_average_marks.studentID) AS average_marks FROM
(SELECT studentID, [subject], marks 
FROM examResult) AS student_average_marks
LEFT JOIN
student
ON
student_average_marks.studentID = student.studentID) AS student_average_marks) AS unique_average_marks
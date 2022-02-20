SELECT TOP(1) Math_Score.studentID AS studentID, studentName, [subject], marks FROM
((SELECT studentID, [subject], marks FROM examResult 
WHERE subject = 'Maths') AS Math_Score
LEFT JOIN
student
ON
Math_Score.studentID = student.studentID)
ORDER BY marks DESC

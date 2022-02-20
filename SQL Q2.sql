SELECT TOP(1) English_Score.studentID AS studentID, studentName, [subject], marks FROM
((SELECT studentID, [subject], marks FROM examResult 
WHERE subject = 'English') AS English_Score
LEFT JOIN
student
ON
English_Score.studentID = student.studentID)
ORDER BY marks

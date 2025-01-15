SELECT AVG(gr.grade) AS average_grade
FROM grades gr
JOIN subjects sub ON gr.subject_id = sub.id
WHERE sub.teacher_id = 1;
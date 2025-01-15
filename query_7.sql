SELECT s.name AS student_name, gr.grade, gr.date
FROM students s
JOIN grades gr ON s.id = gr.student_id
WHERE s.group_id = 1 AND gr.subject_id = 1;
SELECT sub.name AS subject_name
FROM subjects sub
JOIN grades gr ON sub.id = gr.subject_id
WHERE gr.student_id = 1;
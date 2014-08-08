SELECT * FROM survey AS s
  JOIN (SELECT task_id, question_id FROM answer WHERE user_id = 2) AS a
  ON s.task_id != a.task_id OR s.question_id != a.question_id
  WHERE s.tally < s.max_tally

FROM survey 
  JOIN (SELECT answer.task_id AS task_id, answer.question_id AS question_id FROM answer WHERE answer.user_id = :user_id_1) AS anon_1 
  ON survey.task_id != anon_1.task_id AND survey.question_id != anon_1.question_id 
  WHERE survey.tally < survey.max_tally

SELECT * FROM survey AS s
  JOIN (SELECT task_id, question_id FROM answer WHERE user_id = 2) AS a
  ON s.task_id != a.task_id OR s.question_id != a.question_id
  WHERE s.tally < s.max_tally

FROM survey 
  JOIN (SELECT answer.task_id AS task_id, answer.question_id AS question_id FROM answer WHERE answer.user_id = :user_id_1) AS anon_1 
  ON survey.task_id != anon_1.task_id AND survey.question_id != anon_1.question_id 
  WHERE survey.tally < survey.max_tally


# Tallies of all tasks
  SELECT count(*)-1 AS tallies, task_id, question_id 
  FROM answer 
  WHERE (value is not null OR user_id = 0)
  GROUP BY task_id, question_id

# Tasks performed by user x
  SELECT task_id, question_id FROM answer
  WHERE user_id = 13
  GROUP BY task_id, question_id

  SELECT task_id, question_id FROM answer AS a
  WHERE user_id = 13
  GROUP BY task_id, question_id

SELECT answer.id AS answer_id, answer.user_id AS answer_user_id, answer.task_id AS answer_task_id, answer.question_id AS answer_question_id, answer.value AS answer_value, answer.timestamp AS answer_timestamp, answer.ip_address AS answer_ip_address 
FROM answer 
JOIN (
  SELECT answer.user_id AS user_id, min(answer.task_id) AS task_id 
  FROM answer 
  WHERE answer.user_id = 1 AND answer.value IS NULL
) AS anon_1 ON answer.user_id = anon_1.user_id AND answer.task_id = anon_1.task_id


SELECT task.id 
  FROM task AS T 
  JOIN answer AS A 
    ON T.id = A.task_id
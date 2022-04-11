class Queries:
  def __init__(self):
    pass
  
  @staticmethod
  def get_user_by_id(id):
    return f'SELECT * FROM users s WHERE s.id = {id}'

  @staticmethod
  def get_all_users():
    return f'SELECT * FROM users'
  
  @staticmethod
  def get_all_courses():
    return f'SELECT * FROM courses'
  
  @staticmethod
  def get_course_by_id(id):
    return f'SELECT * FROM courses c WHERE c.id = {id}'

  @staticmethod
  def get_all_challenges():
    return f'SELECT * FROM challenges'
  
  @staticmethod
  def get_challenge_by_course_id(id):
    return f'SELECT * FROM challenges ch WHERE ch.course_id = {id}'
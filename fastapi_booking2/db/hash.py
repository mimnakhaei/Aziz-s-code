from passlib.context import CryptContext

# Set up the CryptContext with bcrypt as the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class Hash:
#     #@staticmethod
#     # Hash the password using bcrypt
#     def bcrypt(password: str) -> str:
#         return pwd_context.hash(password)

#     #@staticmethod
#     def verify(plain_password: str, hashed_password: str) -> bool:
#         # Verify a plain password against a hashed password.
#         return pwd_context.verify(plain_password, hashed_password)

class Hash():
 def bcrypt(password: str):
  return pwd_context.hash(password)
 
 def verify(hashed_password, plain_password):
  return pwd_context.verify(plain_password, hashed_password)

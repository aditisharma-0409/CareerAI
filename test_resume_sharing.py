
from backend.database.operations import request_resume_sharing

success, message = request_resume_sharing(
    resume_id=3,
    user_id=3,
    company_id=1,
    admin_id=1
)

print("Success:", success)
print("Message:", message)

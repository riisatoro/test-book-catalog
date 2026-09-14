# Notes
- - -


TODO:

1. Security
Books should use UUID4 instead of autoincremental ID


2.Validation
User password length & complexity, year for author and book should not be negative
Book should have name with minimal length of 1 character.


3. Unit tests
Verify endpoint authorization requirement
Verify users can't edit books they're not own or edit other profiles


4. Dockerization
Add PostgreSQL database and configuration for quick deployment.
Prepare dev, staging and production configuration to easily deploy different version of application


5. Ordering in queries
Verify all GET API using ordering
Add create_at & update_at datetime field for each record


6. Optimization
Add indexes for books list for quick requests
Add workers for uvicorn to handle concurrent requests


7. Further development
Books can have additional fields, like description
Books can have genres, setting (m2m relationship)
S3 for book cover images 
Books can have multiple authors (m2m relationship)
Author and user profile should be separated - this way when user deletes profile, we keep author information and books related to it (right now if author is deleted, all records deleted CASCADE)
Admin dashboard for managing records

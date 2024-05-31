# Login Server
### FastAPI 를 활용한 로그인 및 JWT토큰 발급 서버 구현

#### POST /login
FastAPI를 활용하여 로그인 및 JWT토큰 발급 서버를 구현하였습니다.
사용자는 해당 서버에 로그인요청을 보내 JWT토큰을 발급 받을 수 있습니다. 
발급된 JWT토큰은 Android 클라이언트의, Shared Preferences에 적재되어 다른 API에 접근할때 인증토큰으로 사용됩니다. 

SQLAlchemy를 활용하여 RDS의 MySQL과 통신하여 로직을 수행할 수 있도록 구축하였습니다. 

Docker를 활용하여 로컬에서 구축한 이후, AWS EC2서버에 올려 배포하였습니다. 

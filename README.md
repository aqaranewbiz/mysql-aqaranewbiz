# MySQL MCP 서버

이 프로젝트는 Smithery의 Model Context Protocol (MCP)을 사용하여 MySQL 데이터베이스와 상호작용하는 서버입니다.

## 주요 기능

- MySQL 데이터베이스 연결 및 쿼리 실행
- MCP 프로토콜을 통한 표준화된 API 제공
- FastAPI 기반의 RESTful API 엔드포인트
- 환경 변수를 통한 설정 관리

## 시작하기

### 필수 요구사항

- Python 3.11 이상
- MySQL 서버
- Docker (선택사항)

### 환경 설정

1. `.env` 파일 생성:
```env
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=your_database_name
```

### 설치 방법

1. 저장소 클론:
```bash
git clone [repository-url]
cd @MCP-Server-for-Smithery
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

### 실행 방법

1. 직접 실행:
```bash
python mcp_server.py
```

2. Docker로 실행:
```bash
docker build -t mysql-mcp-server .
docker run -e MYSQL_HOST=host -e MYSQL_USER=user -e MYSQL_PASSWORD=pass -e MYSQL_DATABASE=db mysql-mcp-server
```

## API 엔드포인트

### 서버 정보 조회
```
GET /status
```
서버의 상태와 사용 가능한 도구 목록을 반환합니다.

### 쿼리 실행
```
POST /execute
```
MySQL 쿼리를 실행하고 결과를 반환합니다.

## 개발 가이드

### 프로젝트 구조
```
@MCP-Server-for-Smithery/
├── mcp_server.py      # 메인 서버 코드
├── requirements.txt   # Python 의존성
├── Dockerfile        # Docker 설정
└── .env              # 환경 변수 (템플릿)
```

### 새로운 기능 추가

1. `mcp_server.py`에 새로운 도구 추가
2. 필요한 의존성 `requirements.txt`에 추가
3. Docker 이미지 재빌드 (Docker 사용 시)

## 문제 해결

### 일반적인 문제

1. 연결 오류:
   - MySQL 서버가 실행 중인지 확인
   - 환경 변수가 올바르게 설정되었는지 확인

2. 쿼리 실행 오류:
   - SQL 구문 검사
   - 데이터베이스 권한 확인

### 로깅

서버는 기본적으로 로그를 표준 출력에 기록합니다. Docker를 사용하는 경우 로그를 확인하려면:
```bash
docker logs [container-id]
```

## 기여하기

1. 이슈 생성
2. 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치 푸시 (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 연락처

문의사항이 있으시면 이슈를 생성해주세요. 
https://fastapi.tiangolo.com/ko/python-types/<br>
https://velog.io/@cho876/%EC%9A%94%EC%A6%98-%EB%9C%A8%EA%B3%A0%EC%9E%88%EB%8B%A4%EB%8A%94-FastAPI
https://wikidocs.net/175092
https://velog.io/@shangrilar/FastAPI-%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0


# FastAPI란?
FastAPI는 API를 만들기 위한 파이썬 웹 프레임워크이다. FastAPI는 이름에 걸맞게 빠른 속도를 자랑한다.

파이썬 웹 프레임워크 중 가장 유명한 django와 flask는 주로 웹 서비스를 만들때 사용한다.<br>
하지만 FastAPI는 <b><span style="color:#fc7514">API를 만드는데 보다 집중한 프레임워크이다.</span></b><br>

django나 flask로 웹 프레임워크를 개발하고, API를 만들었다면 각 플랫폼마다 매칭되는 API를 따로 해줘야한다. 예를들어, 
FastAPI로 작성한 API는 React나 Vue.js, Svelte와 같은 Frontend 웹 프레임워크에서 사용할 수 있고 안드로이드나 아이폰 앱에서도 사용할 수 있다. 만약 django나 flask로 웹 서비스를 만들었다면 이에 대응하는 안드로이드나 아이폰 앱을 위한 API 개발을 따로 해야 하지만 FastAPI는 한번 만든 API를 여러 클라이언트에서 변경없이 사용할 수 있다.

django나 flask로 API를 못만드는 것은 아니다. 다만, API를 작성하는 데에는 FastAPI가 좀 더 유리하다. django에도 FastAPI와 비슷한 역할을 하는 DRF(Django REST Framework)가 있다.

<hr>

### uvicorn이란?
uvicorn은 async/await을 기반한 비동기 프로그래밍 지원, 퍼포먼스가 가장 좋다고 알려진 ASGI이다.
본 페이지 내, 실행 결과에 대해 확인하기 위한 용도로 설치

`uvicorn main:app --reload`
`univorn`: 서버 실행을 위해 기본적으로 기재해야하는 명령어
`main`: 실행할 초기 파이썬 파일 이름. 만약 실행 소스코드 파일 이름이 index.py였다면 index:app으로 수정해줘야 한다.
`app`: FastAPI()모듈을 할당한 객체명을 기재한다. 만약, start=FastAPI()라고 위에서 실행했었다면 여기서도 main:start라고 기재해줘야 정상 실행한다.
`reload`: 소스코드가 변경되었을 시, 서버를 자동으로 재시작해주는 옵션

uvicorn으로 app 실행 후 swagger 페이지 보려면 뒤에 `/docs` 붙이면 됨.


###  Pydantic
`BaseModel`은 라이브러리의 클래스로, 데이터 유효성 검사 및 설정을 위해 사용된다.<br>
Pydantic은 FastAPI와 함께 사용되며, FastAPI는 이를 통해 요청 데이터의 유효성 검사를 자동으로 처리한다.
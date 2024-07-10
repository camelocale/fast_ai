<!-- <script>
  let message;

  fetch("http://127.0.0.1:8000").then((response) => {
    response.json().then((json) => {
      message = json.message;
    });
  });
</script>

<h1>{message}</h1> -->


<!-- <script>
  let question_list = []

  function get_question_list() {
    fetch("http://127.0.0.1:8000/api/question/list").then((response) => {
      response.json().then((json) => {
        question_list = json
      })
    })
  }

  get_question_list()
</script> -->


<!-- svelte의 each문을 순회하면서 subject를 출력함 -->
<!-- question_list를 state 변수로 지정하지 않아도 question_list 값이 변경되는 순간 화면에 실시간으로 반영된다. -->

<!-- <ul>
  {#each question_list as question}
    <li>{question.subject}</li>
  {/each}
</ul> -->

<script>
  import Router from 'svelte-spa-router'
  import Home from './routes/Home.svelte'
  import Detail from './routes/Detail.svelte'
  import QuestionCreate from './routes/QuestionCreate.svelte'
  import Navigation from './components/Navigation.svelte'
  import UserCreate from './routes/UserCreate.svelte'
  import UserLogin from './routes/UserLogin.svelte'
  import QuestionModify from './routes/QuestionModify.svelte'
  import AnswerModify from './routes/AnswerModify.svelte'

  const routes = {
    '/': Home,
    '/detail/:question_id': Detail, // 여기서 가변적인 변수 :question_id를 넣어줌으로써 export let params = {} 를 통해 svelte 파일에서 사용할 수 있다.
    '/question-create': QuestionCreate,
    '/user-create':UserCreate,
    '/user-login': UserLogin,
    '/question-modify/:question_id': QuestionModify,
    '/answer-modify/:answer_id': AnswerModify,
  }
</script>

<Navigation/>
<Router {routes}/>
<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router' // a 태그에 use:link 속성을 사용하기 위해 link를 import 했다. 
    import { page, is_login } from "../lib/store"

    let question_list = []
    let size = 10
    // let page = 0 
    let total = 0
    // $: 기호를 붙이면 해당 변수는 반응형 변수가 되는데, api 호출로 인해 total 변수의 값이 변하면 total_page 값 역시 실시간으로 다시 계산된다. 
    $: total_page = Math.ceil(total/size)

    function get_question_list(_page) {
      let params = {
        page: _page,
        size: size,
      }
      fastapi('get', '/api/question/list', params, (json) => {
        question_list = json.question_list
        $page = _page
        total = json.total
      })
    }

  
    // original code
    // function get_question_list() {
    //   fetch("http://127.0.0.1:8000/api/question/list").then((response) => {
    //     response.json().then((json) => {
    //       question_list = json
    //     })
    //   })
    // }

    // function get_question_list() {
    //   fastapi('get', '/api/question/list', {}, (json) => {
    //     question_list = json.question_list //operantion, url, params, success_callback
    //   })
    // }
  
    $: get_question_list($page)
  </script>
  
  
  <!-- svelte의 each문을 순회하면서 subject를 출력함 -->
  <!-- question_list를 state 변수로 지정하지 않아도 question_list 값이 변경되는 순간 화면에 실시간으로 반영된다. -->
  
  <!-- a 태그에 use:link를 사용하면 경로에 #문자가 선행되도록 경로가 만들어져서 새로고침을 했을 때 같은 페이지로 인식해서 서버(현재 경로는 프론트엔드에서만 사용해서 백엔드에 같은 경로로 요청을 보내면 404오류가 뜸)로 요청을 다시 보내지 않는다.  -->

  <!-- <ul>
    {#each question_list as question}
      <li><a use:link href="/detail/{question.id}">{question.subject}</a></li> 
    {/each}
  </ul> -->

  <div class="container my-3">
    <table class="table">
        <thead>
        <tr class="text-center table-dark">
            <th>번호</th>
            <th style="width:50%">제목</th>
            <th>작성자</th>
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        {#each question_list as question, i}
        <tr class="text-center">
            <td>{i+1}</td>
            <td class="text-start">
                <a use:link href="/detail/{question.id}">{question.subject}</a>
            </td>
            <td>{ question.user ? question.user.username : "" }</td>
            <td>{question.create_date}</td>
        </tr>
        {/each}
        </tbody>
    </table>

    <ul class="pagination justify-content-center">
      <li class="page-item {$page <= 0 && 'disabled'}">
        <button class="page-link" on:click="{() => get_question_list(0)}">처음으로</button>
      </li>
      <!-- 이전 페이지 --> 
      <li class="page-item {$page <= 0 && 'disabled'}">
        <!-- 이전 페이지가 없으면 비활성 -->
        <button class="page-link" on:click="{() => get_question_list($page-1)}">이전</button>
      </li>
      <!-- 페이지 번호 -->
      {#each Array(total_page) as _, loop_page}
      {#if loop_page >= $page-5 && loop_page <= $page+5}
      <li class="page-item {loop_page === $page && 'active'}">
        <!-- 페이지가 현재 페이지와 같으면 활성화 -->
        <button on:click="{() => get_question_list(loop_page)}" class="page-link">{loop_page+1}</button>
      </li>
      {/if}
      {/each}
      <!-- 다음 페이지 -->
      <li class="page-item {$page >= total_page-1 && 'disabled'}">
        <!-- 다음 페이지가 없으면 비활성  -->
        <button class="page-link" on:click="{() => get_question_list($page+1)}">다음</button>
      </li>
      <li class="page-item {$page >= total_page-1 && 'disabled'}">
        <button class="page-link" on:click="{() => get_question_list(total_page-1)}">마지막으로</button>
      </li>
    </ul>


    <a use:link href="/question-create" class="btn btn-primary {$is_login ? '' :'disabled'}">질문 등록하기</a>
</div>
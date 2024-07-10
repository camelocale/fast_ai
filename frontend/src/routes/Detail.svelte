<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { link, push } from 'svelte-spa-router'
    import { is_login, username } from  "../lib/store"
    import { access_token } from "../lib/store.js"
    import { get } from 'svelte/store'
    import { tick } from 'svelte'
    import { onMount, afterUpdate } from 'svelte'
    import { marked } from 'marked'

    export let params = {} //Detail 컴포넌트를 호출할 때 전달한 파라미터 값을 읽으려면 params 변수를 선언해야 한다. 
    // console.info(params)
    let question_id = params.question_id
    // console.info('question_id:' + question_id)

    let question = {answers:[]}
    let content = ""
    let error = {detail:[]}
    let real_streamingContent = ""
    let buf = ""
    let isLoading = false // 로딩 상태를 저장할 변수
    let first = true
    let messageContainer
    let shouldScroll = false;
    // let markdown = ""

    async function scrollToBottom() {
        await tick(); // DOM이 업데이트될 때까지 기다림
        if (messageContainer) {
            // 스크롤을 맨 아래로 이동
            messageContainer.scrollTo({
                top: messageContainer.scrollHeight,
                behavior: 'smooth'
            });
        }
        console.info("scroll")
    }

    onMount(() => {
        get_question();
        scrollToBottom();
    });

    afterUpdate(() => {
        if (shouldScroll) {
            scrollToBottom();
            shouldScroll = false;
        }
    });

    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json => {
            question=json
        }))
    }

    get_question()

    async function post_answer(content) {
        // event.preventDefault() // form 태그에서 자동으로 api가 전송되는 것을 방지하기 위함이다. 
        console.info("post_answer")
        let create_url = "/api/answer/create/" + question_id
        let params = {
            content: content 
        }
        
        return new Promise((resolve, reject) => {
            fastapi('post', create_url, params,
                (json) => {
                    get_question()
                    console.info("post_answer 완료")
                    error = {detail: []}
                    resolve()
                },
                (err_json) => {
                    error = err_json
                    reject(err_json)
                }
            )
            })
    }

    async function generate_answer(content) {
        // event.preventDefault() // form 태그에서 자동으로 api가 전송되는 것을 방지하기 위함이다. 
        console.info("here is generate_answer")
        let generate_url = "/api/answer/generate/" + question_id
        let prev_streamingContent = ""
        let streamingContent = ""
        real_streamingContent = ""
        buf = ""
        first = true
        
        
        isLoading = true
        const _access_token = get(access_token)
        
        // return new Promise((resolve, reject) => {
        //     let gen = fastapi('post', generate_url, params,
        //         (json) => {
        //             get_question()
        //             console.info("generate_answer 완료")
        //             resolve()
        //         },
        //         (err_json) => {
        //             error = err_json
        //             reject(err_json)
        //         }
        //     )
        // })

        try {
            let headers = {
                'Content-Type': 'application/json'
            }
            
            if (_access_token) {
                headers["Authorization"] = "Bearer " + _access_token
            }

            const response = await fetch(generate_url, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({ content })
            })

            
            // while (true) {
            //     const { done, value } = await reader.read()
            //     console.info(done, value)
            //     if (done) break
            //     streamingContent = decoder.decode(value, { stream: true })
            //     console.info(streamingContent)
            //     console.info("\n")
            //     await tick()
            // }
            const decoder = new TextDecoder()
            
            const writableStream = new WritableStream({
                write(chunk) {
                    streamingContent = decoder.decode(chunk, { stream: true })
                    if (first === true) {
                        streamingContent = ""
                        real_streamingContent = ""
                        first = false
                    }else if (prev_streamingContent.length > streamingContent.length && streamingContent.length <= 2) {
                        buf += prev_streamingContent
                        buf += " "
                        first = true
                        console.info(buf)
                        console.info(prev_streamingContent, prev_streamingContent.length, streamingContent, streamingContent.length)
                    }
                    prev_streamingContent = streamingContent
                    real_streamingContent = buf + streamingContent
                    shouldScroll = true
                },
                close() {
                    console.info("generate_answer 완료")
                    isLoading = false // 로딩 상태 종료
                },
                abort(err) {
                    console.error("Streaming error: ", err)
                    error = { detail: [err.message] }
                    isLoading = false // 로딩 상태 종료
                }
            })

            await response.body.pipeTo(writableStream)
        } catch (err) {
            console.error("Streaming error: ", err)
            error = {detail: [err.message]}
            isLoading = false // 로딩 상태 종료
        }
        return real_streamingContent
    }

    async function click_handler(event) {
        let streaming_result = ""
        event.preventDefault()
        console.info("click handler 호출됨")
        try {
            let content_reserve = content
            await post_answer(content);
            shouldScroll = true;
            content = ''
            streaming_result = await generate_answer(content_reserve);
            shouldScroll = true;
            console.info(streaming_result)
            await post_answer(streaming_result);
            shouldScroll = true;
        } catch (err) {
            console.error(err)
        }
    }

    function delete_question(_question_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/question/delete"
            let params = {
                question_id: _question_id
            }
            fastapi('delete', url, params, 
                (json) => {
                    push('/')
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    function delete_answer(_answer_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/answer/delete"
            let params = {
                answer_id: _answer_id
            }
            fastapi('delete', url, params, 
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

</script>

<style>
    .container {
        display: flex;
        flex-direction: column;
        height: 95vh; /* Viewport height를 기준으로 전체 높이를 설정 */
        width: 100vw; /* Viewport width를 기준으로 전체 너비를 설정 */
        overflow: hidden; /* 전체 뷰포트를 벗어나는 내용이 보이지 않도록 설정 */
    }
  
    .content-container {
        display: flex;
        flex-direction: column;
        flex: 1; /* 남은 공간을 차지하도록 설정 */
        overflow: hidden;
    }

    #message-container {
        flex: 1; /* 남은 공간을 차지하도록 설정 */
        overflow-y: auto; /* 세로 스크롤 가능하도록 설정 */
    }
    
    form {
      flex-shrink: 0; /* 폼의 크기가 줄어들지 않도록 설정 */
    }
</style>

<div class="container">
<div class="content-container">
<div class="container my-3" id="message-container" bind:this={messageContainer}>
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{question.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{question.content}</div>
            <div class="d-flex justify-content-end">
                {#if question.modify_date }
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{question.modify_date}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{ question.user ? question.user.username : ""}</div>
                    <div>{question.create_date}</div>
                </div>
            </div>
            <div class="my-3">
                {#if question.user && $username === question.user.username }
                <a use:link href="/question-modify/{question.id}"
                    class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-seondary"
                    on:click={() => delete_question(question.id)}>삭제</button>
                {/if}
            </div>
        </div>
    </div>

    <button class="btn btn-secondary" on:click="{() => {push('/')}}">
        목록으로
    </button>

    <!-- 답변 목록 -->
    <h5 class="border-bottom my-3 py-2">{question.answers.length}개의 답변이 있습니다.</h5>
    {#each question.answers as answer}
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{@html marked(answer.content)}</div>
            <div class="d-flex justify-content-end">
                {#if answer.modify_date }
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{answer.modify_date}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{ answer.user ? answer.user.username : ""}</div>
                    <div>{answer.create_date}</div>
                </div>
            </div>
            <div class="my-3">
                {#if answer.user && $username === answer.user.username }
                <a use:link href="/answer-modify/{answer.id}" 
                    class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_answer(answer.id) }>삭제</button>
                {/if}
            </div>
        </div>
    </div>
    {/each}
    <!-- 실시간 스트리밍 결과 표시 -->
    {#if isLoading}
        <div class="streaming-content my-3 p-3 border rounded">
            <div>{@html marked(real_streamingContent)}</div>
        </div>
    {/if}
    <!-- 답변 등록 -->
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} disabled={$is_login ? "": "disabled"} class="form-control" />
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary {$is_login ? "": "disabled"}" on:click="{click_handler}" />
    </form>
</div>
</div>
</div>
/**
 *  Echo WebSocket
 */
var ws1 = new WebSocket('ws://' + document.domain + ':' + location.port + '/ws')

ws1.onmessage = function(event) {
    addMessage('messages', event.data)
}

ws1.onerror = (error) => {
    reportError('echo', error)
}

var button1 = document.getElementById('send')
button1.onclick = () => {
    var content = document.getElementById('input').value
    ws1.send(content)
}

/**
 * Broadcast Websocket
 */
var ws2 = new WebSocket('ws://' + document.domain + ':' + location.port + '/api/v2/ws')

ws2.onopen = (event) => {
}

ws2.onmessage = (event) => {
    addMessage('broadcast', event.data)
}

ws2.onclose = (event) => {

}

ws2.onerror = (error) => {
    reportError('broadcast', error)
}

/**
 * Helper
 */

function addMessage(list_id, message) {
    var list_dom = document.getElementById(list_id)
    var message_dom = document.createElement('li')
    var content_dom = document.createTextNode(message)
    message_dom.appendChild(content_dom)
    list_dom.appendChild(message_dom)
}

function reportError(tag, error) {
    if(error != null) {
        var errors_dom = document.getElementById('errors')
        var term_dom = document.createElement('dt')
        var term_text = document.createTextNode(tag)
        var descr_dom = document.createElement('dd')
        var descr_text = document.createTextNode(error.message)
        term_dom.appendChild(term_text)
        descr_dom.appendChild(descr_text)
        errors_dom.appendChild(term_dom)
        errors_dom.appendChild(descr_dom)
    }
}
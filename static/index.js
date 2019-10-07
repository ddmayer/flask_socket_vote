document.addEventListener('DOMContentLoaded', () => {
    namespace = '/test';
    const room_code = location.pathname.split('/')[1];
    // Connect to websocket
    //var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    var socket = io(namespace);
    
    // When connected, configure buttons
    socket.on('connect', () => {
        // join room
        socket.emit('join',{'room_code':room_code})

        // Each button should emit a "submit vote" event
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                const selection = button.dataset.vote;
                console.log(selection);
                socket.emit('submit vote', {'room_code': room_code, 'selection': selection});
            };
        });
    });

    // When a new vote is announced, add to the unordered list
    socket.on('vote totals', data => {
        console.log('vote totals')
        document.querySelector('#yes').innerHTML = data.yes;
        document.querySelector('#no').innerHTML = data.no;
        document.querySelector('#maybe').innerHTML = data.maybe;
    });
});

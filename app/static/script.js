var socket = io();
socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});

socket.on('detection_data', function (data) {
  console.log("detection_data", data)
})


















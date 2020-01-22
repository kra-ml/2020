new function() {
    var ws = null;
    var connectionStatus;
    var sendButton;

    var open = function() {
        var url = serverUrl.val();
        ws = new WebSocket(url);
        ws.onopen = onOpen;
        ws.onclose = onClose;
        ws.onmessage = onMessage;
        ws.onerror = onError;

        connectionStatus.text('OPENING ...');
        serverUrl.attr('disabled', 'disabled');
        connectButton.hide();
        disconnectButton.show();
    }

    var onOpen = function() {
        console.log('OPENED: ' + serverUrl.val());
        connected = true;
        connectionStatus.text('OPENED');
        sendMessage.removeAttr('disabled');
        sendButton.removeAttr('disabled');
    };


    var onMessage = function(event) {
        var data = event.data;
        addMessage(data);
    };

    var onError = function(event) {
        alert('Server Down');
    }

    var addMessage = function(data, type) {

    }

    WebSocketClient = {
        init: function() {
            open();
            sendMessage = $('#site');

            sendButton = $('#bt');

            sendButton.click(function(e) {
                var msg = $('#sendMessage').val()
                alert(msg)
                    //ws.send(msg);
            });

        }
    };
}
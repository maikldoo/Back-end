var api = function (method, params) {
    params = params || {}
    var settings = {
        "method": "POST",
        "type": "POST",
        "headers": {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        "body": JSON.stringify({
            "method": method,
            "params": params
        })
    };

    return fetch('/api/', settings)
        .then(response=> {
           
            return response.json()
        })
        .then(res=>{
            if (res.error) {
                Modal.showModal({
                    title: res.error,
                    buttons: [{
                        className: 'btn-primary',
                        text: 'ОК',
                        clickButton: function () {
                            Modal.close();
                        }
                    }]
                });
                throw new Error(res.error);
            }
            return res.result
        });
}

var dowlandApi = function (method, params) {
    params = params || {}
    var settings = {
        "method": "POST",
        "type": "POST",
        "headers": {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        "body": JSON.stringify({
            "method": method,
            "params": params
        })
    };

    return fetch('/api/', settings)
        .then(response=> {
            return response.blob()
        }).then(blob=> {
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = "members.xlsx";
            document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
            a.click();    
            a.remove();  //afterwards we remove the element again      
        })
}
//Utility functions for working with URL parameters

function getURLParams() {
    if (window.location.search) {
        var queryParams = window.location.search.substring(1).split("&");
        return queryParams.map(function(n) {
            n = n.split("=");
            this[n[0]] = n[1];
            return this;
        }.bind({}))[0];
    } else {
        return {};
    }
}

function setURLParams(obj) {
    if (Object.keys(obj) && Object.keys(obj).length) {
        var queryString = Object.keys(obj).map(function(n) {
            return n + "=" + obj[n];
        }).join("&");
        window.location.search = queryString;
    } else {
        window.location.search = "";
    }
}

function setURLParam(key, value) {
    var params = getURLParams();
    params[key] = value;
    setURLParams(params);
}



var modal = function () {
    this.showModal = function (params) {
        params = params || {};
        this.title(params.title);
        this.buttons(params.buttons);
        this.body(params.body);
        this.show(true);
    }
    this.close = function (params) {
        this.show(false)
    }
    this.show = ko.observable(false);
    this.title = ko.observable();
    this.buttons = ko.observable();
    this.body = ko.observable();
}
var Modal = new modal();

ko.applyBindings(Modal, document.getElementById("modal"));
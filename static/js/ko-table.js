function tableModel (items, filter, options) {
    var self = this;
    this._options = options || {idProperty: "id"}
    var _items = items;
    
    function pageChange() {
        self.items(_items.slice((this.page - 1)*self.countPage(), self.countPage()*this.page));
    }
   
    function renderPaging(_items) {
        _items = _items || items;
        var paging = [];
        for (var i = 1; i <= Math.ceil(_items.length / self.countPage()); i++) {
            paging.push({
                page: i,
                pageChange: pageChange
            })
        }
        if (paging.length > 1) {
            self.paging(paging);
        } else {
            self.paging([])
        }
    }
    
    this._filter = function() {
        var search = self.search();
        var x = filter(items, search);
        self.items(x.slice(0, self.countPage()))
        renderPaging(x);
    }
    
    this.items = ko.observableArray(items.slice(0, 10));
    this.paging = ko.observable();
    this.countPage = ko.observable(10);
    this.search = ko.observable();
    renderPaging();
    
    this.remove = function() {
        if (self._options.objects) {
        
             Modal.showModal({
                title: "Вы действительно хотите удалить?",
                buttons: [
                    {
                        className: ' btn-secondary',
                        text: 'Нет',
                        clickButton: function () {
                            Modal.close();
                        }
                    },{
                        className: ' btn-primary',
                        text: 'Да',
                        clickButton: () => {
                            api(self._options.objects + ".delete", {id: this[options.idProperty]}).then(res => {
                                self.items.remove(this);
                                delete _items[_items.indexOf(this)]; 
                                delete items[items.indexOf(this)]; 
                                self.items(self.items());
                                
                                Modal.showModal({
                                    title: "Запись удалена",
                                    buttons: {
                                        className: ' btn-primary',
                                        text: 'ОК',
                                        clickButton: function () {
                                            Modal.close();
                                        }
                                    }
                                });
                            });
                            
                        }
                    }
                ]
            })
        
            
        } else {
            console.log("not objects")
        }
    }
    
    this.update = function() {
        if (self._options.objects) {
            location.assign("/manager/" + self._options.objects + "/" + "update" + "/" + "?id=" + this[options.idProperty] )
        } else {
            console.log("not objects")
        }
    }
    
    this.startSearch = function() {
        self._filter()
    }
    this.countPage.subscribe(function (value) {
        self.items(_items.slice(0, value));
        self._filter();
    });
    
}

odoo.define('web.ChangeBackground', function (require) {
"use strict";

var session = require('web.session');

var def  = new $.Deferred();
var url = session.url('/web/image', {
            model: 'res.company',
            id: session.company_id,
            field: 'background_image',
        });
var url_navbar = session.url('/web/image', {
            model: 'res.company',
            id: session.company_id,
            field: 'navbar_image',
        });
session.rpc('/web/dataset/search_read', {
    model: 'res.company',
    domain: [['id','=',session.company_id]],
}, {
    timeout: 3000,
    shadow: true,
})
.then(function(results){
        if(results.length){
        if(results.records[0].background_image){
            def.resolve();
        }else{
            def.reject();
        }
    }
}, function(type,err){
    def.reject();
    console.log(err);
});
def.done(function () {
    function myLoop () {
       setTimeout(function () {
          $("div.o_application_switcher").css({
                "background-image": "url(" + url + ")",
                "background-size": "cover"
            });
          $("div.o_main_navbar").css({
                "background-image": "url(" + url_navbar + ")",
                "background-size": "cover"
            });
          if ($("div.o_application_switcher").length <= 0) {
             myLoop();
          }
       }, 1000)
    }
    myLoop();
});

});
(function () {
    function my$(id) {
        return document.getElementById(id);
    }
    var box =my$("box");
    var hd=box.getElementsByTagName("div")[0];
    var bd=box.getElementsByTagName("div")[1];
    var list = bd.getElementsByTagName("li");
    var spans =hd.getElementsByTagName("span");
    for (var i = 0;i<spans.length;i++){
        spans[i].setAttribute("index",i);
        spans[i].onclick=function () {
            for (var j= 0;j<spans.length;j++){
                spans[j].removeAttribute("class");
            }
            this.className="current"
            var num = this.getAttribute("index");
            for (var k=0;k<list.length;k++) {
                list[k].removeAttribute("class");
            }
            list[num].className="current";
        }
    }
})();

window.onload = function(){
    CKEDITOR.replace( 'editor1' );
}
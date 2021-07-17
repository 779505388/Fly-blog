
$('#back-top-btn').click(()=>{
    window.scrollTo({ 
        top: 0, 
        behavior: "smooth" 
    });
})
$(document).scroll(()=>{
    $('.mdui-progress-determinate').css('width',($(document).scrollTop()/($(document.body).height()-$(window).height())).toFixed(3)*100+'%')
if($(document).scrollTop()>$(window).height()){
    
    $('#back-top-btn').fadeIn()
}else{
    $('#back-top-btn').fadeOut()
}

})
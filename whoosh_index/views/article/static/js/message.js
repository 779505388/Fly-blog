
$('.vat').click(function () {
    let comment = ($(this).parent().parent().children('.vreply-wrapper')[0]);
    $(comment).append($('.vwrap')[0])
    let nick = ($(this).parent().parent().children('.vhead').children('.vnick').html());
    let uuid = $(this).parent().parent().children('.vhead').children('.vnick').attr('id')
    if (!uuid){
        uuid = $(this).parent().parent().parent().parent().parent().children('.vhead').children('.vnick').attr('id')
    }
    $('#veditor').attr('placeholder', '@ ' + nick);
    $('input[name="parent"]').val(null)
    $('input[name="captcha"]').val(null)
    $('#veditor').val(null)
    $('input[name="parent_uuid"]').val(uuid);
    $('input[name="parent_name"]').val(nick);
})


$('.vsubmit').click(function () {
    let type = 'message'
    let parentId = $('input[name="parent"]').val()
    let nick = $('input[name="nick"]').val()
    let mail = $('input[name="mail"]').val()
    let link = $('input[name="link"]').val()
    let captcha = $('input[name="captcha"]').val()
    let text = $('#veditor').val()
    let parent_uuid = $('input[name="parent_uuid"]').val()
    let parent_name = $('input[name="parent_name"]').val()
    let articleId = 0
    if (!nick) {
        mdui.snackbar({
            message: '昵称为空',
            position: 'right-top'
        });
        return false
    }
    if (!mail) {
        mdui.snackbar({
            message: '邮箱为空',
            position: 'right-top'
        });
        return false
    }
    if (!text) {
        mdui.snackbar({
            message: '回复内容为空',
            position: 'right-top'
        });
        return false
    }
    if (!captcha) {
        mdui.snackbar({
            message: '验证码为空',
            position: 'right-top'
        });
        return false
    }
    let data = {
        nick,
        mail,
        link,
        text,
        captcha,
        type,
        parentId,
        articleId,
        parent_name,
        parent_uuid
    }

    $.post("/comment/", data, function (data, status)  {
        if(data.status ==='success') {
            localStorage.setItem('nick', nick);
            localStorage.setItem('mail', mail);
            localStorage.setItem('link', link);
            location.reload();
        }else{
            mdui.snackbar({
                message: data.message,
                position: 'right-top'
            })
        }
    });
})

$('#captcha').click(()=>{
    $('#captcha').attr("src", '/api/v1/captcha/?'+new Date().getTime());
})

$('#review-btn').click(()=>{
    $('.vpanel')[0].append($('.vwrap')[0])
    $('#veditor').attr('placeholder', '想对我说些什么呢');
    $('input[name="parent"]').val(null)
    $('input[name="captcha"]').val(null)
    $('#veditor').val(null)
    $('input[name="parent_uuid"]').val(null);
    $('input[name="parent_name"]').val(null);
})
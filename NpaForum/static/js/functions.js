//加入收藏
function addFav(ele) {
    var fav_type = ele.attr('data-fav-type')
    var data_id = ele.attr('data-fav-id')

    $.ajax({
        cache: false,
            type: 'post',
            url: '/add_fav/',
            data : {'fav_type': fav_type,
                    'data_id': data_id},
            async: false,
            beforeSend:function (xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken )
            },
            success:function (data) {
                if(data.success){
                    ele.html(data.text)
                }else{
                    alert('操作失败')
                }
            }
    })
}


(function () {
  var $image = $('#image'); // 模态框

  var $modal = $('.modal');
  var imgUrl = '';
  var cropper = null; // 初始裁切

  $image.cropper({
    aspectRatio: 16 / 9
  });
  cropper = $image.data('cropper');
  $('#uploadFile').change(function (e) {
    var reads = new FileReader();
    f = e.target.files[0];
    reads.readAsDataURL(f);

    reads.onload = function (e) {
      $image.attr('src', this.result);
      $image.cropper('destroy');
      $image.cropper({
        aspectRatio: 16 / 9
      });
      cropper = $image.data('cropper');
    };
  });
  $('#chkUpload').click(() => {
    if ($('.my-canvas').attr('id')) {
      $('.my-canvas')[0].remove();
    }

    $('.layer').show();
    $('#chkUpload, .file-wrap').hide(); // 参数：设置输出图片的高度
    // width, height, minWidth, minHeight,

    var myCanvas = cropper.getCroppedCanvas({
      // 最小高度和宽度
      // 具体多少宽度你可以设置
      width: 300,
      height: 200
    }); // 预览盒子的类名

    myCanvas.className = 'box-center my-canvas';
    $modal.append(myCanvas);
    imgUrl = myCanvas.toDataURL('image/png');
  });
  $('#uploadImg').click(e => {
    e.preventDefault();
    var formData = new FormData();
    var file = dataURLtoFile(imgUrl, 'image'); // 指定图片的文件加格式, 不指定图片无文件后缀, 因为图片是base64位编码

    file.name = 'image.png'; // 后端接收文件参数的名字

    formData.append('file', file);
    $.ajax({
      type: 'post',
      // 上传地址
      url: 'http://localhost',
      processData: false,
      contentType: false,
      data: formData,

      success(res) {
        // 上传成功后回调
        console.log(res);
      },

      error(err) {
        // 上传失败后后回调
        console.log(err);
      }

    });
  }); // 关闭

  $('.close, #exit').click(() => {
    $('.layer').hide();
    $('.my-canvas')[0].remove();
    $('#chkUpload, .file-wrap').show();
  }); // 把64位编码转换为file对象

  function dataURLtoFile(dataurl, filename) {
    var arr = dataurl.split(','),
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]),
        n = bstr.length,
        u8arr = new Uint8Array(n);

    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }

    return new File([u8arr], filename, {
      type: mime
    });
  }
})();

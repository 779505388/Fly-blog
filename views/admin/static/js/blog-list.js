var app = new Vue({
  delimiters: ["{[", "]}"],
  el: "#app",
  data: {
    artcleList: null
  },
  mounted() {
    axios
      .post("{{url_for('admin.blog_list')}}")
      .then(
        response =>
          (this.artcleList = response.data)
          // console.log(response.data)
      )
      .catch(function(error) {
        // 请求失败处理
        console.log(error);
      });
  }
});

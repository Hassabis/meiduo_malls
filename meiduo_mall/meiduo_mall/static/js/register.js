let vm = new Vue({
	el:'#app',//绑定HTML内容
	delimiters: ['[[',']]'],
	data:{//数据对象
		//v-model
		username:'',
		password:'',
		password2:'',
		mobile:'',
		allow:'',
		image_code:'',
		sms_code:'',
		uuid:'',
		image_code_url:'',


		// v-show
		error_name:false,
		error_password:false,
		error_check_password:false,
		error_phone:false,
		error_allow:false,
		error_image_code:false,

		//error_message
		error_message:'',
		error_mobile_message:'',
	},
	mounted(){
		this.generate_image_code();
	},
	methods:{//定义事件和实现方法 采用的是es6的写法
		//图形验证码,封装思想，进行代码复用
		generate_image_code(){
			this.uuid = new Date().getTime();
			// this.uuid = 'e1b6120f-053b-42a0-9926-28eb8f1400b6';
			this.image_code_url = '/image_codes/' + this.uuid + '/';
		},
		check_username(){
			//用户名是5-20个字符 [a-zA-Z0-9_-]
			//定义正则
			let re = /^[a-zA-Z0-9_-]{5,20}$/;
			if (re.test(this.username)){
				this.error_name = false;
			}else {
				//匹配失败,展示错误信息
				this.error_message = '请输入5-20个字符的用户名';
				this.error_name = true;
			}
			if (this.error_name == false){
				let url = '/usernames/' + this.username + '/count/';
				axios.get(url,{
					responseType:'json'
				}).then(response =>{
					if (response.data.count == 1){
						this.error_message = '用户名已经存在';
						this.error_name = true;
					}else {
						this.error_name = false;
					}
				}).catch(error =>{
					console.log(error.data)
				})
			}
		},
		check_pwd(){
			//校验密码
			let re = /^[0-9A-Za-z]{8,20}$/;
			if (re.test(this.password)){
				this.error_password = false;
			}else {
				this.error_password = true;
			}
		},
		check_cpwd(){
			//验证两次密码是否一致
			if (this.password2 != this.password){
				this.error_check_password = true;
			}else {
				this.error_check_password = false;
			}
		},
		check_phone(){
			if (this.mobile.length < 11 || this.mobile.length > 11){
				this.error_phone = true;
				this.error_mobile_message = '手机号码不符合预期'
			}else {
				this.error_phone = false;
			}
			if (this.error_phone == false){
				let url = '/phone/' + this.mobile + '/count/';
				axios.get(url,{
					responseType: 'json'
				}).then(response =>{
					if (response.data.count == 1){
						this.error_mobile_message = '手机号已被注册';
						this.error_phone = true;
					}else {
						this.error_phone = false;
					}
				}).catch(error=>{
					console.log(error.data)
				})
			}
		},
		check_sms_code(){

		},
		check_allow(){
			if(!this.allow){
				this.error_allow = true;
			}else {
				this.error_allow = false;
			}
		},
		check_image_codes(){
			if (this.image_code.length < 4){
				this.error_image_code = true;
			}else {
				this.error_image_code = false;
			}
		},
		on_submit(){
			this.check_username();
			this.check_pwd();
			this.check_cpwd();
			this.check_mobile();
			this.check_allow();

			if (this.error_name == true || this.error_password == true || this.error_check_password == true || this.error_mobile == true || this.error_allow == true){
				window.event.returnValue = false
			}
		}
	}
});
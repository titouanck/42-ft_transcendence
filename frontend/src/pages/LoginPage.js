import React from 'react'

const LoginPage = () => {
  return (
	<div>
		<form>
		  <input type='text' name='username' placeholder='some_username'></input>
		  <input type='password' name='password' placeholder='some_password'></input>
		  <input type='submit'></input>
	  </form>
	</div>
  )
}

export default LoginPage

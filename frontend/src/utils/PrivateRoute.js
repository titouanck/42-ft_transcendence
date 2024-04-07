import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ redirectPath, element }) => {
	console.log('PrivateRoute works!')
	const authenticated = false;
	

	return authenticated ? element : <Navigate to={redirectPath} />;
}

export default PrivateRoute;

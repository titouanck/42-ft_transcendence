import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import PrivateRoute from './utils/PrivateRoute'

import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import Header from './component/Header';

function App() {
	return (
		<div className="App">
			<BrowserRouter>
				<Header/>
				<Routes>
					<Route exact path="/" element={
						<PrivateRoute element={<HomePage />} redirectPath="/login" />
					} />
					<Route element={<LoginPage/>} path="/login" />
				</Routes>
			</BrowserRouter>
		</div>
	);
}

export default App;

import {useState} from "react";
import {Instance} from "./http/Instance";
import {Link, Route, Routes} from "react-router-dom";
import Main from "./components/Main";
import Login from "./components/Login";
import Register from "./components/Register";
import Cart from "./components/Cart";
import Orders from "./components/Orders";
import './css/bootstrap.min.css';
import './css/style.css'

function App() {

    const [token, setToken] = useState(null)
    const [title, setTitle] = useState('')

    const logout = async () => {
        await Instance('logout', 'GET', token)
        setToken(null)
    }


    return (
        <div className="container py-3">
            <header>
                <div className="d-flex flex-column flex-md-row align-items-center pb-3 mb-4 border-bottom">
                    <Link to="/" className="d-flex align-items-center text-dark text-decoration-none">
                        <span className="fs-4">«MyShop»</span>
                    </Link>

                    <nav className="d-inline-flex mt-2 mt-md-0 ms-md-auto">
                        {
                            token ?
                                <>
                                    <Link className="me-3 py-2 text-dark text-decoration-none" to="/orders">Мои
                                        заказы</Link>
                                    <Link className="me-3 py-2 text-dark text-decoration-none" to="/cart">Корзина</Link>
                                    <Link onClick={() => logout()} className="me-3 py-2 text-dark text-decoration-none"
                                          to="/">Выйти</Link>
                                </>
                                :
                                <>
                                    <Link className="me-3 py-2 text-dark text-decoration-none"
                                          to="/register">Регистрация</Link>
                                    <Link className="me-3 py-2 text-dark text-decoration-none"
                                          to="/login">Авторизация</Link>
                                </>
                        }
                    </nav>
                </div>

                <div className="pricing-header p-3 pb-md-4 mx-auto text-center">
                    <h1 className="display-4 fw-normal">{title}</h1>
                </div>
            </header>
            <Routes>
                <Route index element={<Main setTitle={setTitle} token={token}/>}/>
                <Route path={'login'} element={<Login setToken={setToken} setTitle={setTitle}/>}/>
                <Route path={'register'} element={<Register setTitle={setTitle}/>}/>
                <Route path={'cart'} element={<Cart setTitle={setTitle} token={token}/>}/>
                <Route path={'orders'} element={<Orders setTitle={setTitle} token={token}/>}/>

            </Routes>
            <footer className="pt-4 my-md-5 pt-md-5 border-top">
                <div className="row">
                    <div className="col-12 col-md">
                        <small className="d-block mb-3 text-muted">&copy; 2017–2021</small>
                    </div>
                </div>
            </footer>
        </div>
    );
}

export default App;

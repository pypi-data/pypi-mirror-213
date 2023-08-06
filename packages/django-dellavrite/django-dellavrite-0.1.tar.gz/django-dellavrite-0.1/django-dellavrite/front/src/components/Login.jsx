import React, {useEffect} from 'react';
import {useState} from "react";
import {Instance} from "../http/Instance";
import {Link, useNavigate} from "react-router-dom";

const Login = ({setToken, setTitle}) => {

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState(false)

    const navigate = useNavigate()

    const login = () => {
        Instance('login', 'POST', null, {
            email: email,
            password: password
        }).then(res => res.ok ? res.json().then(data => {
                    setToken(data.data.user_token)
                    navigate('/')
                })
                : res.json().then(data => setError(data.error))
        )
    }

    useEffect(() => {
        setTitle('Авторизация')
    }, [])


    return (
        <main>
            <div className="row row-cols-1 row-cols-md-3 mb-3 text-center justify-content-center">
                <div className="col">
                    <div className="row">
                        <form onSubmit={e => {
                            e.preventDefault();
                            login()
                        }}>
                            <span style={{color: 'red'}}>{error.message}</span>
                            <div className="form-floating mb-3">
                                <input
                                       value={email} onChange={e => setEmail(e.target.value)} type="email"
                                       className="form-control" id="floatingInput"
                                       placeholder="name@example.com"/>
                                <label htmlFor="floatingInput">Email</label>
                                <span style={{color: 'red'}}>{error.errors?.email}</span>
                            </div>
                            <div className="form-floating mb-3">
                                <input
                                    value={password} onChange={e => setPassword(e.target.value)} type="password"
                                    className="form-control" id="floatingPassword"
                                    placeholder="Password"/>
                                <label htmlFor="floatingPassword">Password</label>
                                <span style={{color: 'red'}}>{error.errors?.password}</span>
                            </div>

                            <button className="w-100 btn btn-lg btn-success mb-3" type="submit">Войти</button>
                            <Link to={'/'} className="w-100 btn btn-lg btn-outline-secondary" type="submit">Назад</Link>
                        </form>
                    </div>

                </div>
            </div>
        </main>
    );
};

export default Login;